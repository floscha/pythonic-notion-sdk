from typing import TYPE_CHECKING, Union

from notion.model import Page
from notion.model.common.utils import UUIDv4

if TYPE_CHECKING:
    from notion.api.client import NotionClient


class PagesEndpoint:
    def __init__(self, client: "NotionClient"):
        self._client = client

    def get(self, page_id: Union[UUIDv4, str]) -> Page:
        "Get a single Notion page by its ID."
        response = self._client._make_request("get", f"pages/{page_id}")
        return Page(data=response).with_client(self._client)

    def create(self, page: Union[Page, dict]) -> Page:
        "Create a new Notion page."
        page_data = page.to_json() if isinstance(page, Page) else page
        response = self._client._make_request("post", "pages", page_data)
        return Page(data=response).with_client(self._client)

    def update(self, page_id: Union[UUIDv4, str], payload: dict) -> Page:
        "Update properties of an existing Notion page."
        response = self._client._make_request("patch", f"pages/{page_id}", payload)
        return Page(data=response).with_client(self._client)

    def delete(self, page_id: Union[UUIDv4, str]) -> Page:
        """Deletes the Notion Page with the given ID.

        The Notion API does not offer a DELETE method but insteads works by setting the `archived` field.
        """
        return self.update(page_id, {"archived": True})
