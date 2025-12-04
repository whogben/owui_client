from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from owui_client.client import OpenWebUI

class Shortcuts:
    """
    A collection of convenience methods (shortcuts) that combine multiple API calls
    into single, easy-to-use workflows.
    
    Access these via `client.shortcuts`.
    """
    def __init__(self, client: "OpenWebUI"):
        self.client = client

