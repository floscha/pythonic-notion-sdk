from typing import TYPE_CHECKING, Optional, Union

from notion.model.blocks import Block
from notion.model.properties.uuidv4 import UUIDv4

if TYPE_CHECKING:
    from notion.api.client import NotionClient


class BlocksEndpoint:
    def __init__(self, client: "NotionClient"):
        self._client = client

    def update(self, block_id: Union[UUIDv4, str], payload: dict):
        "Update properties of an existing Notion page."
        return self._client._make_request("patch", f"blocks/{block_id}", payload)

    def retrieve_children(
        self, block_id: Union[UUIDv4, str], limit: Optional[int] = None
    ) -> list[dict]:
        "Retrieve children of a given block."
        response = self._client._make_request("get", f"blocks/{block_id}/children")
        assert isinstance(response, dict)
        return response["results"]

    def append_children(
        self, block_id: Union[UUIDv4, str], children: list[Union[Block, dict]]
    ):
        "Append children blocks to an existing block"
        children = [
            child.to_json() if isinstance(child, Block) else child for child in children
        ]
        return self._client._make_request(
            "patch", f"blocks/{block_id}/children", {"children": children}
        )

    def delete(self, block_id: Union[UUIDv4, str]):
        """Deletes the Notion Block with the given ID.

        The Notion API does not offer a DELETE method but insteads works by setting the `archived` field.
        """
        return self.update(block_id, {"archived": True})
