from typing import TYPE_CHECKING, Optional, Union

from notion.model import Database, Page
from notion.model.filters import Filter
from notion.model.properties.uuidv4 import UUIDv4

if TYPE_CHECKING:
    from notion.api.client import NotionClient


class DatabasesEndpoint:
    def __init__(self, client: "NotionClient"):
        self._client = client

    def get(self, database_id: Union[UUIDv4, str]) -> Database:
        "Get a single Notion database by its ID."
        data = self._client._make_request("get", f"databases/{database_id}")
        assert isinstance(data, dict)
        return Database.from_json(data).with_client(self._client)

    def query(
        self,
        database_id: Union[UUIDv4, str],
        filter_: Optional[Union[Filter, dict]] = None,
        sort: Optional[dict] = None,
    ) -> list[Page]:
        "Query a Notion database for pages given some filter(s)."
        filter_ = {
            "filter": filter_.to_json() if isinstance(filter_, Filter) else filter_
        }
        data = self._client._paginate(
            "post", f"databases/{database_id}/query", {**filter_, **(sort or {})}
        )
        return [
            Page.from_json(page_data).with_client(self._client) for page_data in data
        ]

    def create(
        self,
        database: Database,
        parent: Optional[Union[UUIDv4, str]] = None,
    ):
        "Create a new Notion database."
        if parent:
            database._data["parent"] = {"type": "page_id", "page_id": parent}

        # Remove "type" key. Otherwise database creation will fail.
        del database._data["type"]

        response = self._client._make_request("post", "databases", database._data)
        database._data = response
        database._client = self._client

    def update(self, database_id: Union[UUIDv4, str], payload: dict) -> Database:
        "Update properties of an existing Notion database."
        data = self._client._make_request("patch", f"databases/{database_id}", payload)
        assert isinstance(data, dict)
        return Database.from_json(data).with_client(self._client)

    def delete(self, page_id: Union[UUIDv4, str]):
        """Deletes the Notion Page with the given ID.

        The Notion API does not offer a DELETE method but insteads works by setting the `archived` field.
        """
        return self.update(page_id, {"archived": True})
