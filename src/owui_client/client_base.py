from typing import TypeVar, Type, List, Any, overload, get_origin, get_args, Union
from httpx import AsyncClient, HTTPStatusError, RequestError
from pydantic import BaseModel

T = TypeVar("T")


class OWUIClientBase:
    """Base class for the OWUIClient, provides the built-in and internal functionality."""

    def __init__(
        self, api_url: str = "http://127.0.0.1:8080/api", api_key: str | None = None
    ):

        self.api_url = api_url
        """The full URL to the Open WebUI API, including the port if it is not 80/443, e.g. http://127.0.0.1:8080/api for local."""

        self.api_key: str | None = api_key
        """The API key to send with requests (if any)."""

        self.__client: AsyncClient | None = None

    @property
    def _client(self) -> AsyncClient:
        """Obtains and configures the httpx client."""
        if not self.__client:
            self.__client = AsyncClient()
        self.__client.base_url = self.api_url
        if self.api_key:
            self.__client.headers.update({"Authorization": f"Bearer {self.api_key}"})
        elif "Authorization" in self.__client.headers:
            del self.__client.headers["Authorization"]
        return self.__client

    @overload
    async def _request(
        self, method: str, url: str, model: Type[T], **kwargs
    ) -> T | List[T]: ...

    @overload
    async def _request(
        self, method: str, url: str, model: None = None, **kwargs
    ) -> Any: ...

    async def _request(
        self, method: str, url: str, model: Type[T] | None = None, **kwargs
    ) -> T | List[T] | Any:
        """
        Wraps the httpx client to request the API.

        If 'model' is provided, attempts to parse the JSON response into that Pydantic model.
        Handles both single objects and lists of objects.
        """
        try:
            response = await self._client.request(method, url, **kwargs)
            response.raise_for_status()

            if model is bytes:
                return response.content

            try:
                data = response.json()
            except ValueError:
                # Return text if response is not JSON
                return response.text

            if model:
                # Handle Optional[T] (which is Union[T, NoneType])
                origin = get_origin(model)
                if origin:
                    args = get_args(model)
                    
                    # Handle List[T]
                    if origin is list:
                        item_type = args[0]
                        if isinstance(data, list):
                            return [
                                self._process_model_item(item_type, item) 
                                for item in data
                            ]
                        # If data is not a list but model expects list, return as is (or raise?)
                        return data

                    # Handle Union[T, None] (Optional)
                    # If it's an Optional (Union with NoneType), find the non-None type
                    # Simplified logic: usually Optional[T] has 2 args, one is T and one is NoneType
                    valid_model = next(
                        (arg for arg in args if arg is not type(None)), None
                    )
                    if valid_model:
                        # If data is None and it's optional, return None
                        if data is None:
                            return None
                        # Use the valid model for validation
                        model = valid_model
                
                # Handle standard models
                return self._process_model_item(model, data)

            return data

        except HTTPStatusError as e:
            # Attempt to extract a more specific error message from the API response
            try:
                error_data = e.response.json()
                detail = None

                if isinstance(error_data, dict):
                    # Open WebUI common error patterns: {"detail": ...} or {"error": ...}
                    if "detail" in error_data:
                        detail = error_data["detail"]
                    elif "error" in error_data:
                        detail = error_data["error"]
                        # Sometimes error is a dict like {"error": {"detail": "..."}}
                        if isinstance(detail, dict):
                            detail = detail.get("detail", str(detail))

                if detail:
                    # Update the exception args to include the detail for better logging/debugging
                    e.args = (f"{e.args[0]} - Details: {detail}",) + e.args[1:]
            except ValueError:
                # Response wasn't JSON, stick to the original error
                pass
            raise e

        except RequestError as e:
            # Handle connection errors, timeouts, etc.
            raise e

    def _process_model_item(self, model: Any, data: Any) -> Any:
        """Helper to process a single item against a model type."""
        if isinstance(model, type) and issubclass(model, BaseModel):
            if isinstance(data, list):
                return [model.model_validate(item) for item in data]
            if data is None:
                return None
            return model.model_validate(data)
        
        # Handle Unions (e.g. Union[ModelA, ModelB])
        origin = get_origin(model)
        if origin is get_origin(Union[int, str]): # Check if it's a Union
             # Try to validate against each type in the Union
             args = get_args(model)
             for arg in args:
                 try:
                     return self._process_model_item(arg, data)
                 except (ValueError, TypeError, AttributeError):
                     continue
             # If none match, return data as is or raise?
             # For now return data to avoid crashing, or let it crash later
             return data

        # Handle primitive types or other classes
        if isinstance(data, list):
            # If model is not a list type but data is list, try to map?
            # This path is ambiguous. 
            # If we are here, model is scalar type, data is list.
            # e.g. model=int, data=[1, 2] -> [1, 2] (list of ints)
            # But we don't know if we should return list[int] or if it's an error.
            # Assuming list mapping:
            try:
                return [model(item) for item in data]
            except TypeError:
                return data
        
        try:
            return model(data)
        except TypeError:
            return data


class ResourceBase:
    """Base class for all resource clients (Auths, Chats, etc)."""

    def __init__(self, client: OWUIClientBase):
        self._client = client

    @overload
    async def _request(
        self, method: str, url: str, model: Type[T], **kwargs
    ) -> T | List[T]: ...

    @overload
    async def _request(
        self, method: str, url: str, model: None = None, **kwargs
    ) -> Any: ...

    async def _request(
        self, method: str, url: str, model: Type[T] | None = None, **kwargs
    ) -> T | List[T] | Any:
        """Delegates the request to the main client instance."""
        return await self._client._request(method, url, model=model, **kwargs)
