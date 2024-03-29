from typing import Any, Dict, List, Optional, Union

import requests

from notion.model.common.utils import UUIDv4
from notion.model.databases.database import Database
from notion.model.filters import Filter
from notion.model.page import Page

API_BASE_URL = "https://api.notion.com/v1/"
API_VERSION = "2022-02-22"


class NotionClient:
    def __init__(self, token: str):
        self.token = token

    def _make_request(self, request_type: str, entity, payload=None) -> dict:
        url = f"{API_BASE_URL}{entity}/"

        headers = {
            "Accept": "application/json",
            "Notion-Version": API_VERSION,
            "Content-Type": "application/json",
            "Authorization": self.token,
        }

        assert request_type in ("get", "post", "patch", "delete")
        requests_func = getattr(requests, request_type)

        response = requests_func(
            url,
            headers=headers,
            json=payload,
        )
        if response.status_code != 200:
            raise ValueError(response.text)

        return response.json()

    def _paginate(
        self,
        request_type: str,
        entity: str,
        payload: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None,
    ) -> List[dict]:
        if payload is None:
            payload = {}

        results = []
        start_cursor = {}
        has_more = True
        while has_more and (not limit or len(results) < limit):
            result_set = self._make_request(
                request_type, entity, {**payload, **start_cursor}
            )
            results.extend(result_set["results"])
            start_cursor = {"start_cursor": result_set.get("next_cursor")}
            has_more = result_set.get("has_more", False)

        return results[:limit]

    # ---------------------------------------------------------------------------
    # Databases
    # ---------------------------------------------------------------------------

    def get_database(self, database_id) -> Database:
        "Get a single Notion database by its ID."
        data = self._make_request("get", f"databases/{database_id}")
        return Database.from_json(data).with_client(self)

    def query_database(
        self,
        database_id,
        filter_: Optional[Union[Filter, dict]] = None,
        sort: Optional[dict] = None,
    ) -> List[Page]:
        "Query a Notion database for pages given some filter(s)."
        filter_ = {
            "filter": filter_.to_json() if isinstance(filter_, Filter) else filter_
        }
        data = self._paginate(
            "post", f"databases/{database_id}/query", {**filter_, **(sort or {})}
        )
        return [Page.from_json(page_data).with_client(self) for page_data in data]

    def create_database(self, database: Database, parent_id: Optional[UUIDv4] = None):
        "Create a new Notion database."
        if parent_id:
            database._data["parent"] = {"type": "page_id", "page_id": parent_id}
        response = self._make_request("post", "databases", database._data)
        database._data = response
        database._client = self

    def update_database(self, database_id, payload: dict) -> dict:
        "Update properties of an existing Notion database."
        return self._make_request("patch", f"databases/{database_id}", payload)

    def delete_database(self, page_id):
        """Deletes the Notion Page with the given ID.

        The Notion API does not offer a DELETE method but insteads works by setting the `archived` field.
        """
        return self.update_database(page_id, {"archived": True})

    # ---------------------------------------------------------------------------
    # Pages
    # ---------------------------------------------------------------------------

    def get_page(self, page_id):
        "Get a single Notion page by its ID."
        data = self._make_request("get", f"pages/{page_id}")
        return Page(client=self, data=data)

    def create_page(self, page: Union[Page, dict]) -> Page:
        "Create a new Notion page."
        page_data = page.to_json() if isinstance(page, Page) else page
        response = self._make_request("post", "pages", page_data)
        return response

    def update_page(self, page_id, payload: dict):
        "Update properties of an existing Notion page."
        return self._make_request("patch", f"pages/{page_id}", payload)

    def delete_page(self, page_id):
        """Deletes the Notion Page with the given ID.

        The Notion API does not offer a DELETE method but insteads works by setting the `archived` field.
        """
        return self.update_page(page_id, {"archived": True})

    # ---------------------------------------------------------------------------
    # Blocks
    # ---------------------------------------------------------------------------

    def update_block(self, block_id, payload: dict):
        "Update properties of an existing Notion page."
        return self._make_request("patch", f"blocks/{block_id}", payload)

    def retrieve_block_children(self, block_id: str, limit: Optional[int] = None):
        "Retrieve children of a given block."
        return self._make_request("get", f"blocks/{block_id}/children")

    def append_block_children(self, block_id: str, children: str):
        "Append children blocks to an existing block"
        return self._make_request(
            "patch", f"blocks/{block_id}/children", {"children": children}
        )

    def delete_block(self, block_id: str):
        """Deletes the Notion Block with the given ID.

        The Notion API does not offer a DELETE method but insteads works by setting the `archived` field.
        """
        return self.update_block(block_id, {"archived": True})

    # ---------------------------------------------------------------------------
    # Search
    # ---------------------------------------------------------------------------

    def search(
        self,
        query: str,
        sort: dict = None,
        filter: Optional[dict] = None,
        limit: Optional[int] = None,
    ) -> Page:
        "Search for Notion pages in all workspaces and databases."
        payload = {"query": query}
        if sort:
            payload["sort"] = sort
        if filter:
            payload["filter"] = filter

        results = self._paginate("post", "search", payload, limit)
        return [Page.from_json(page_data).with_client(self) for page_data in results]
