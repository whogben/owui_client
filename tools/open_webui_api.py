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

  *AUTO-UPDATE*
  This tool will automatically update itself by default - checking once per 6 hours on the first tool call.
  - Autoupdate requires that the tool have an API key with write permissions for itself.
  - You can disable auto-update by setting the autoupdate_tool valve to False, it will still check for updates and notify the AI.
  - You can change the URL where updates come from (for example, to your own github file rather than mine.)
  - You can adjust the interval at which updates are checked by setting the version_check_interval valve.
  - By default, auto-update runs at the end of a tool call - your initial tool call will be run with the current version, then the next call will be on the new version.
  As this tool is new, and issues are expected, it is recommended to leave auto-update enabled, so that you get any fixes asap.

  *USE AT YOUR OWN RISK!*
  This is a pre-release, it is very plausible that your AI can use this to break your Open WebUI instance.
  - Don't run it on prod unless you've got a good backup strategy in place.
  - Inspect all AI tool calls marked "call_api", and abort the AI if it's acting suspiciously.
  - Report any issues at https://github.com/open-webui/owui_client/issues

required_open_webui_version: 0.6.0
requirements: --upgrade, owui-client<2.0, httpx<1.0
version: 0.3.0
license: MIT
"""

import ast
import asyncio
import inspect
import json
import os
import re
import sys
import time
from packaging.version import parse as parse_version
from typing import Any, Callable

from httpx import AsyncClient, HTTPStatusError
from pydantic import BaseModel, Field

from owui_client import OpenWebUI
from owui_client.client_base import ResourceBase
from owui_client.models.tools import ToolModel, ToolForm


class Tools:

    class Valves(BaseModel):

        default_openwebui_api_url: str = Field(
            "",
            description="Default Open WebUI API URL, e.g. http://<ip or url>:8080/api. \
                Leave blank to require users set their own.",
        )
        default_openwebui_api_key: str = Field(
            "",
            description="Default Open WebUI API Key. Leave blank to require users set their own.",
        )
        autoupdate_tool: bool = Field(
            default=True,
            description="Whether to automatically update the tool when a new version is available. \
                Set to False to disable automatic updates. (You'd better trust that the tool_source_url is safe!). \
                If set to False, an AI that calls any tool will be notified if an update is available alongside every tool response.",
        )
        version_check_interval: int = Field(
            default=21600,
            description="How often to check for new tool versions, in seconds. Default of 21600 seconds = 6 hours. \
                Set to 0 to check every tool run, or -1 to disable version checks.",
        )
        tool_source_url: str = Field(
            default="https://raw.githubusercontent.com/whogben/owui_client/refs/heads/main/tools/open_webui_api.py",
            description="URL of the tool script used for update checks. Set to blank to disable update checks. \
                Set to a custom URL to use a different tool script for update checks.",
        )
        local_storage_path: str = Field(
            default="/app/backend/data/open_webui_api_tool_state.json",
            description="Path to the local file used to store state between runs. \
                (Uninstalling the tool does not delete this file, you will need to manually delete it if you want to start fresh.)",
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
        Inspects the current context, returning metadata about the current chat (including it's folder hierarchy), current user, and current model (thats you!).
        Use this when you need to act on the user, the chat, or yourself - to find out the appropriate ids.
        Note that inspect_context (and any other tool) may optionally include additional_data with the api_result.
        Additional data may contain information such as version_check_result in the response,
        notifying if there is a new version available, or if a new version was installed.
        Unless the user has explicitly told you not to, you should raise this information to them prominently.
        """
        owui = _get_api(self)

        # Obtain additional context that we may need in parallel
        get_user = owui.users.get_user_by_id(__metadata__["user_id"])
        get_chat = owui.chats.get(__metadata__["chat_id"])

        user_info, chat_info = await asyncio.gather(get_user, get_chat)

        # Extract and combine user information into it's own dict
        __metadata__["user"] = {
            "id": __metadata__.pop("user_id"),
            "name": user_info.name,
            "email": user_info.email,
            "role": user_info.role,
        }

        # Build the folder inheritance chain to find all influences on the chat
        current_folder_id = chat_info.folder_id
        folders = []  # Collect folders in order from immediate parent to root

        while current_folder_id:
            folder_info = await owui.folders.get_folder_by_id(current_folder_id)

            folder_files = folder_info.data.get("files", [])
            collection_files = [
                file for file in folder_files if file.get("type") == "collection"
            ]
            single_files = [
                file for file in folder_files if file.get("type") != "collection"
            ]

            system_prompt_preview = folder_info.data.get("system_prompt", "")[:140]
            if system_prompt_preview:
                system_prompt_preview += "..."

            folder = {
                "id": folder_info.id,
                "name": folder_info.name,
                "system_prompt_preview": system_prompt_preview,
                "knowledge_file_ct": len(single_files),
                "knowledge_collection_ct": len(collection_files),
            }

            folders.append(folder)
            current_folder_id = folder_info.parent_id

        # Build the nested structure from the collected folders
        # Start with the root folder (last in the list) and nest upwards
        nested_folder = None
        for folder in reversed(folders):
            if nested_folder is None:
                nested_folder = folder
            else:
                # Create a copy of the folder and add the nested parent
                folder_with_parent = folder.copy()
                folder_with_parent["parent_folder"] = nested_folder
                nested_folder = folder_with_parent

        __metadata__["parent_folder"] = nested_folder

        return await _finalize_tool_response(self, __metadata__)

    async def find_apis(
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

        return await _finalize_tool_response(self, results)

    async def get_api_details(
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

        return await _finalize_tool_response(
            self,
            {
                "apis": api_results,
                "schemas": schema_results,
            },
        )

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
        return await _finalize_tool_response(self, convert_basemodel_to_dict(result))


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


def _load_state(self: Tools) -> dict:
    try:
        if not os.path.exists(self.valves.local_storage_path):
            return {}
        with open(self.valves.local_storage_path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}


def _save_state(self: Tools, state: dict):
    if state:
        json_str = json.dumps(state)
        os.makedirs(os.path.dirname(self.valves.local_storage_path), exist_ok=True)
        with open(self.valves.local_storage_path, "w") as f:
            f.write(json_str)
    else:
        if os.path.exists(self.valves.local_storage_path):
            os.remove(self.valves.local_storage_path)


async def _fetch_remote(self: Tools) -> dict:
    """
    Obtains the latest remote tool code and version from the remote tool source URL.
    Raises a descriptive ValueError on failure.
    """
    async with AsyncClient() as client:
        response = await client.get(self.valves.tool_source_url)
        try:
            response.raise_for_status()
        except HTTPStatusError as e:
            raise ValueError(
                f"Error fetching remote tool source from {self.valves.tool_source_url}: {e}"
            )
    remote_code = response.text
    _remote_version = _extract_semver(remote_code)
    if not _remote_version:
        raise ValueError(
            f"Unable to locate version in remote tool source from {self.valves.tool_source_url}"
        )
    return {"code": remote_code, "version": _remote_version}


async def _check_for_updates(
    self: Tools, force_check: bool = False, install_update: bool = False
) -> dict | None:
    """
    Checks for updates if it's time to check, or if force_check is True.
    If an update is available, and install_update is True, installs the update.
    Updates the stored version check state.
    Returns "None" if there is nothing to report, otherwise returns a dict describing actions taken.
    """

    report = {}

    # Obtain saved udpate info
    state = _load_state(self)
    if "update_info" not in state:
        state["update_info"] = {
            "remote_version": "",
            "last_checked": 0,
            "last_updated": 0,
        }
    update_info = state["update_info"]

    # Determine local code version
    local_docstr = sys.modules[self.__module__].__doc__ or ""
    local_version = _extract_semver(local_docstr)
    if not local_version:
        return {"error": "Unable to locate version in local tool source"}

    # Early return if it's not time to check for updates
    if (
        not force_check
        and time.time() - update_info["last_checked"]
        < self.valves.version_check_interval
    ):
        return None

    # Fetch the latest remote tool source and version and update the saved state
    try:
        remote = await _fetch_remote(self)
    except ValueError as e:
        return {"error": str(e)}
    update_info["last_checked"] = time.time()
    update_info["remote_version"] = remote["version"]
    _save_state(self, state)

    # If the remote version is not newer than the local version, return nothing
    if parse_version(update_info["remote_version"]) <= parse_version(local_version):
        return None

    # If we are not tasked with installing the update, return that an update is available
    if not install_update:
        return {
            "Open WebUI API Tool Update Available": {
                "local_version": local_version,
                "remote_version": update_info["remote_version"],
                "tool_source_url": self.valves.tool_source_url,
            }
        }

    # Otherwise, attempt the update
    try:
        await _install_update(self, remote["code"])

        # Save the updated state
        update_info["last_updated"] = time.time()
        _save_state(self, state)

        # Inform the AI that the update was successful
        return {
            "Open WebUI API Tool Updated": {
                "original_version": local_version,
                "new_version": update_info["remote_version"],
                "tool_source_url": self.valves.tool_source_url,
            }
        }
    except ValueError as e:
        return {"error installing update": f"{e}"}


async def _get_own_tool(self: Tools) -> ToolModel:
    """
    Returns the ID of the current tool.
    """
    local_docstr = (sys.modules[self.__module__].__doc__ or "").strip()

    owui = _get_api(self)
    tool_ids = [tool.id for tool in await owui.tools.get_tools()]
    tools = await asyncio.gather(*map(owui.tools.get_tool_by_id, tool_ids))

    for tool in tools:
        if tool and hasattr(tool, "content") and tool.content:
            source_tree = ast.parse(tool.content)
            candidate_docstring = ast.get_docstring(source_tree)
            if candidate_docstring and candidate_docstring.strip() == local_docstr:
                return tool

    raise ValueError(f"Unable to locate own tool ID in the list of tools")


async def _install_update(self: Tools, remote_code: str):
    """
    Overwrites the local tool source with the remote code and returns on success,
    or raises ValueError on failure.
    """

    owui = _get_api(self)

    # Figure out our own tool
    tool = await _get_own_tool(self)

    # Install the update
    try:
        result = await owui.tools.update_tool_by_id(
            tool.id,
            ToolForm(
                id=tool.id,
                name=tool.name,
                content=remote_code,
                meta=tool.meta,
            ),
        )
    except Exception as e:
        raise ValueError(f"Error installing update: {e}")


async def _finalize_tool_response(self: Tools, result: Any) -> dict:
    """Performs universal finalization tasks, including version checking, before returning tool results."""
    response = {"api_result": result}

    if self.valves.version_check_interval >= 0:

        update_info = await _check_for_updates(
            self, force_check=False, install_update=self.valves.autoupdate_tool
        )
        if update_info:
            response.setdefault("additional_info", {})[
                "version_check_result"
            ] = update_info

        state = _load_state(self)

        last_version_check = state.get("version_info", {}).get("last_checked", 0)
        if time.time() - last_version_check > self.valves.version_check_interval:
            await _check_for_updates(self, install_update=False)

    return response


def _extract_semver(tool_code: str) -> str | None:
    """Obtains the a tool script's semver string (just x.y.z portion) from it's frontmatter."""
    # Rules: grabs version from first line that starts with "version: x.x.x"
    pattern = r"^\s*version:\s*(?P<version>\d+\.\d+\.\d+)"
    match = re.search(pattern, tool_code, re.MULTILINE)
    if match:
        return match.group("version")
    return None


_add_api_index_to_find_apis()
