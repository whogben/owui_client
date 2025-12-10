"""
title: Open WebUI API
author: William Hogben
description: |
  Give your Open WebUI agents the ability to manage an Open WebUI insance.

  > The API call.. is coming from inside the house!

  Using this tool your AI agent can call *any* command from the full Open WebUI API.

  *HOW IT WORKS*
  There are 4 tools which provide access to the API:
  - inspect_context lets the AI find out who the user is, what chat it's in, and what model it is.
  - find_apis can be used to search for specific APIs, helping the AI orient itself
  - get_api_details returns the documentation for a given API, along with the schemas of it's parameters
  - call_api is used to send an API command.

  *USE AT YOUR OWN RISK!*
  This is a pre-release, it is very plausible that your AI can use this to break your Open WebUI instance.
  - Don't run it on prod unless you've got a good backup strategy in place.
  - Inspect all AI tool calls marked "call_api", and abort the AI if it's acting suspiciously.
  - Report any issues at https://github.com/open-webui/owui_client/issues

required_open_webui_version: 0.6.0
requirements: pydantic, owui-client
version: 0.2.0
license: MIT
"""

import asyncio
import os
import inspect
from typing import Any, Callable

from owui_client import OpenWebUI
from owui_client.client_base import ResourceBase

from pydantic import BaseModel, Field


class Tools:

    class Valves(BaseModel):

        default_openwebui_api_url: str = Field(
            "",
            description="Default Open WebUI API URL, e.g. http://<ip or url>:8080/api. Leave blank to require users set their own.",
        )
        default_openwebui_api_key: str = Field(
            "",
            description="Default Open WebUI API Key. Leave blank to require users set their own.",
        )

    class UserValves(BaseModel):

        openwebui_api_url: str = Field(
            "", description="Your Open WebUI API URL, e.g. http://<ip or url>:8080/api"
        )
        openwebui_api_key: str = Field("", description="Your Open WebUI API Key")

    def __init__(self):
        self.valves = self.Valves()
        self.user_valves = self.UserValves()

    async def inspect_context(
        self,
        __metadata__: dict = {},
    ) -> dict:
        """
        Inspects the current context, returning metadata about the current chat, current user, and current model (thats you!).
        Use this when you need to act on the user, the chat, or yourself - to find out the appropriate ids.
        """

        # Obtain folder information and inject it into metadata
        owui = _get_api(self)
        chat_info = await owui.chats.get(__metadata__["chat_id"])
        if chat_info.folder_id:
            __metadata__["folder_id"] = chat_info.folder_id
            folder_info = await owui.folders.get_folder_by_id(chat_info.folder_id)
            __metadata__["folder_name"] = folder_info.name
        else:
            __metadata__["folder_id"] = ""
            __metadata__["folder_name"] = ""

        return __metadata__

    def find_apis(
        self,
        query: str = Field(...),
    ) -> list[str]:
        """
        Finds APIs that match a query, or all APIs if no query is provided.
        Use this as your first step when interacting with the Open WebUI API to locate the current, available, APIs that you can use.
        Returns the API signature, as well as the first line of the API's docstring.
        Typically followed by a call to get_apis to get the rest of the API details.
        The optional query parameter is used to filter the APIs by case-insensitive matching of the API name, params, returns, and first line of description.
        """
        results = []

        # dynamically list all resources in the OpenWebUI client
        owui = _get_api(self)
        for resource_name in dir(owui):
            resource = getattr(owui, resource_name)
            if not isinstance(resource, ResourceBase):
                continue

            for method_name in dir(resource):
                if method_name.startswith("_"):
                    continue
                method = getattr(resource, method_name)
                if not callable(method):
                    continue
                docline = ""
                if method.__doc__:
                    for line in method.__doc__.split("\n"):
                        if line.strip():
                            docline = line.strip()
                            break

                # Get parameter information
                params_info = {}
                return_type = "Any"
                try:
                    sig = inspect.signature(method)

                    def simplify_type(type_obj):
                        """Extract just the class name from type objects"""
                        if type_obj == inspect.Parameter.empty:
                            return "Any"
                        elif hasattr(type_obj, "__name__"):
                            # Handle actual class objects
                            return type_obj.__name__
                        elif isinstance(type_obj, str):
                            # Handle string representations
                            if type_obj.startswith("<class '") and type_obj.endswith(
                                "'>"
                            ):
                                # Extract class name from <class 'module.ClassName'>
                                return type_obj.split("'")[1].split(".")[-1]
                            elif "." in type_obj:
                                # For typing module references like typing.Optional[str]
                                return type_obj.split(".")[-1]
                            return type_obj
                        else:
                            # Handle other type objects
                            return (
                                str(type_obj).split(".")[-1].split("'")[0]
                                if "." in str(type_obj)
                                else str(type_obj)
                            )

                    for name, param in sig.parameters.items():
                        param_type = simplify_type(param.annotation)
                        params_info[name] = param_type

                    # Get return type annotation
                    return_type = simplify_type(sig.return_annotation)
                except:
                    params_info = {"error": "Could not inspect parameters"}

                # Format into single string
                params_str = ", ".join(
                    [f"{name}:{param_type}" for name, param_type in params_info.items()]
                )
                formatted_string = f"{resource_name}.{method_name}({params_str}) -> {return_type}, {docline}.."

                results.append(formatted_string)

        # Filter apis by query (case insensitive)
        if isinstance(query, str) and query:
            query_lower = query.lower()
            filtered_apis = []
            for api_string in results:
                if query_lower in api_string.lower():
                    filtered_apis.append(api_string)
            results = filtered_apis

        return results

    def get_api_details(
        self,
        apis: str = Field(...),
    ) -> dict:
        """
        Get the full details of one or more APIs, including their docstring, and the schemas of any params and returns.
        Pass one or more API names in the form of "resource.method", e.g. "auths.get_session_user, chats.create_chat" in the apis parameter.
        """
        api_results = {}
        schema_results = {}

        owui = _get_api(self)

        def enhance_schema_with_descriptions(model_class):
            """Enhance a BaseModel schema with field descriptions from docstrings"""
            if not hasattr(model_class, "__fields__"):
                return model_class.schema()

            schema = model_class.schema()
            if "properties" not in schema:
                schema["properties"] = {}

            # Get the model's source code to extract field descriptions
            try:
                source = inspect.getsource(model_class)
                lines = source.split("\n")

                current_field = None
                current_description = []

                for line in lines:
                    line = line.strip()
                    if line.startswith('"""') or line.startswith("'''"):
                        if current_field and current_description:
                            # Save the description for the current field
                            description = "\n".join(current_description).strip()
                            if current_field in schema["properties"]:
                                schema["properties"][current_field][
                                    "description"
                                ] = description
                            current_field = None
                            current_description = []
                        continue

                    # Check if this line defines a field
                    if (
                        current_field is None
                        and ":" in line
                        and not line.startswith("#")
                    ):
                        # This might be a field definition
                        field_part = line.split(":")[0].strip()
                        if field_part and not field_part.startswith("_"):
                            current_field = field_part
                    elif current_field is not None:
                        # Collect description lines
                        if line and not line.startswith("#"):
                            current_description.append(line)

            except:
                pass  # If we can't get source, just return the basic schema

            return schema

        for api_name in apis.split(","):
            api_name = api_name.strip()
            resource_name, method_name = api_name.split(".")
            resource = getattr(owui, resource_name)
            method = getattr(resource, method_name)

            # Get full method signature
            try:
                sig = inspect.signature(method)
                params_str = ", ".join(
                    [
                        f"{name}: {param.annotation}"
                        for name, param in sig.parameters.items()
                    ]
                )
                return_annotation = sig.return_annotation
                if return_annotation == inspect.Parameter.empty:
                    return_annotation = "Any"
                signature = f"def {method_name}({params_str}) -> {return_annotation}:"
            except:
                signature = "Could not extract signature"

            # Get docstring
            docstring = method.__doc__ or ""

            api_results[api_name] = {
                "signature": signature,
                "docstring": docstring,
            }

            # Extract BaseModel schemas for params and returns with descriptions
            try:
                if sig.parameters:
                    for param_name, param in sig.parameters.items():
                        if (
                            param.annotation != inspect.Parameter.empty
                            and isinstance(param.annotation, type)
                            and issubclass(param.annotation, BaseModel)
                        ):
                            enhanced_schema = enhance_schema_with_descriptions(
                                param.annotation
                            )
                            schema_results[f"{api_name}_{param_name}"] = enhanced_schema

                if (
                    sig.return_annotation != inspect.Parameter.empty
                    and isinstance(sig.return_annotation, type)
                    and issubclass(sig.return_annotation, BaseModel)
                ):
                    enhanced_schema = enhance_schema_with_descriptions(
                        sig.return_annotation
                    )
                    schema_results[f"{api_name}_return"] = enhanced_schema
            except:
                pass  # Silently handle any schema extraction errors

        return {
            "apis": api_results,
            "schemas": schema_results,
        }

    async def call_api(
        self,
        api: str = Field(...),
        params: dict = Field(...),
    ) -> dict:
        """
        Call an Open WebUI API method with the given parameters.
        The api parameter should be in the form "resource.method".
        The params parameter should be a dictionary of parameter values.
        Returns the API result with any BaseModel instances converted to dictionaries.
        VERY IMPORTANT:
        - The Open WebUI API changes rapidly, you cannot rely on training data to be up to date.
        - Use get_api_details to get the full API parameter details in context before calling an API.

        """
        owui = _get_api(self)

        # Parse the API name
        resource_name, method_name = api.split(".")
        resource = getattr(owui, resource_name)
        method = getattr(resource, method_name)

        def convert_basemodel_to_dict(data):
            """Recursively convert BaseModel instances to dictionaries"""
            if isinstance(data, BaseModel):
                return data.model_dump()
            elif isinstance(data, list):
                return [convert_basemodel_to_dict(item) for item in data]
            elif isinstance(data, dict):
                return {
                    key: convert_basemodel_to_dict(value) for key, value in data.items()
                }
            else:
                return data

        def convert_dict_to_basemodel(param_value, target_type):
            """Convert dictionary values to Pydantic model instances"""
            if target_type == inspect.Parameter.empty or not isinstance(
                target_type, type
            ):
                return param_value

            # Check if the target type is a Pydantic BaseModel
            if issubclass(target_type, BaseModel):
                if isinstance(param_value, dict):
                    return target_type(**param_value)
                elif isinstance(param_value, list):
                    return [
                        target_type(**item) if isinstance(item, dict) else item
                        for item in param_value
                    ]
                else:
                    return param_value
            else:
                return param_value

        # Convert params dictionary to include Pydantic model instances where needed
        try:
            sig = inspect.signature(method)
            converted_params = {}

            for param_name, param in sig.parameters.items():
                if param_name in params:
                    # Convert the parameter value to the expected type if it's a BaseModel
                    converted_params[param_name] = convert_dict_to_basemodel(
                        params[param_name], param.annotation
                    )
                elif param.default != inspect.Parameter.empty:
                    # Use default value if parameter not provided
                    converted_params[param_name] = param.default
                elif param.annotation != inspect.Parameter.empty and issubclass(
                    param.annotation, BaseModel
                ):
                    # For required BaseModel parameters that weren't provided, create empty instance
                    converted_params[param_name] = param.annotation()
                else:
                    # For other required parameters that weren't provided, leave as-is (will raise error)
                    converted_params[param_name] = params.get(param_name)

        except Exception as e:
            # If conversion fails, fall back to original params
            converted_params = params

        # Call the API method and handle both sync and async methods
        result = method(**converted_params)
        if asyncio.iscoroutine(result):
            result = await result

        # Convert the result to ensure no BaseModel instances remain
        return convert_basemodel_to_dict(result)


def _get_api(self: Tools, user: dict = {}) -> OpenWebUI:
    # Prioritize UserValves from the injected __user__ dictionary
    user_valves = user.get("valves") if user else None

    url = (
        (user_valves.openwebui_api_url if user_valves else None)
        or self.user_valves.openwebui_api_url
        or self.valves.default_openwebui_api_url
        or os.getenv("OPENWEBUI_API_URL", "")
    )
    key = (
        (user_valves.openwebui_api_key if user_valves else None)
        or self.user_valves.openwebui_api_key
        or self.valves.default_openwebui_api_key
        or os.getenv("OPENWEBUI_API_KEY", "")
    )

    if not url:
        raise ValueError(
            "Open WebUI API URL is missing. Please configure it in User Valves or Global Valves."
        )

    if not key:
        raise ValueError(
            "Open WebUI API Key is missing. Please configure it in User Valves or Global Valves."
        )

    if not url.endswith("/"):
        url += "/"

    return OpenWebUI(url, key)


def _add_api_index_to_find_apis():
    index = ""
    owui = OpenWebUI("http://dummy-url:8080/api", "dummy-key")
    for resource_name in dir(owui):
        resource = getattr(owui, resource_name)
        if not isinstance(resource, ResourceBase):
            continue
        index += f"\n{resource_name}:\n"
        for method_name in dir(resource):
            if method_name.startswith("_"):
                continue
            method = getattr(resource, method_name)
            if not callable(method):
                continue
            index += f"- {method_name}\n"
    Tools.find_apis.__doc__ += (
        "\nAPI Index (Resource.Method):\n\t\t(may include APIs that we don't have permission for)\n"
        + index
    )


_add_api_index_to_find_apis()

print(Tools.find_apis.__doc__)
