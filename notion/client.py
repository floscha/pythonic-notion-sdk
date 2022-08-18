from typing import Any, Dict, List, Optional, Union

import requests

from notion.api import UserEndpoint
from notion.model.comment import Comment
from notion.model.common.types import JSON
from notion.model.common.utils import UUIDv4
from notion.model.databases.database import Database
from notion.model.filters import Filter
from notion.model.page import Page

API_BASE_URL = "https://api.notion.com/v1/"
API_VERSION = "2022-02-22"


class NotionClient:
    """A client class that handles communication with the Notion API.

    Parameters:
        token: The secret of a given Notion integration.
        timeout, proxies, verify: See https://requests.readthedocs.io/en/latest/api/
    """

    def __init__(
        self,
        token: str,
        timeout: Optional[Union[float, tuple]] = None,
        proxies: Optional[dict] = None,
        verify: Union[bool, str] = True,
    ):
        self.token = token

        self.timeout = timeout
        self.proxies = proxies
        self.verify = verify

        # API Endpoints
        self.users = UserEndpoint(self)

    def _make_request(
        self, request_type: str, entity, payload=None, params=None
    ) -> JSON:
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
            params=params,
            timeout=self.timeout,
            proxies=self.proxies,
            verify=self.verify,
        )
        if response.status_code != 200:
            raise ValueError(response.text)

        return response.json()

    def _paginate(
        self,
        request_type: str,
        entity: str,
        payload: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None,
    ) -> List[dict]:
        if payload is None:
            payload = {}

        results: List[dict] = []
        start_cursor: Dict[str, Any] = {}
        has_more = True
        while has_more and (not limit or len(results) < limit):
            result_set = self._make_request(
                request_type, entity, payload={**payload, **start_cursor}, params=params
            )
            assert isinstance(result_set, dict)

            results.extend(result_set["results"])
            start_cursor = {"start_cursor": result_set.get("next_cursor")}
            has_more = result_set.get("has_more", False)

        return results[:limit]

    # ---------------------------------------------------------------------------
    # Databases
    # ---------------------------------------------------------------------------

    def get_database(self, database_id: Union[UUIDv4, str]) -> Database:
        "Get a single Notion database by its ID."
        data = self._make_request("get", f"databases/{database_id}")
        assert isinstance(data, dict)
        return Database.from_json(data).with_client(self)

    def query_database(
        self,
        database_id: Union[UUIDv4, str],
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

    def create_database(
        self, database: Database, parent_id: Optional[Union[UUIDv4, str]] = None
    ):
        "Create a new Notion database."
        if parent_id:
            database._data["parent"] = {"type": "page_id", "page_id": parent_id}
        response = self._make_request("post", "databases", database._data)
        database._data = response
        database._client = self

    def update_database(
        self, database_id: Union[UUIDv4, str], payload: dict
    ) -> Database:
        "Update properties of an existing Notion database."
        data = self._make_request("patch", f"databases/{database_id}", payload)
        assert isinstance(data, dict)
        return Database.from_json(data).with_client(self)

    def delete_database(self, page_id: Union[UUIDv4, str]):
        """Deletes the Notion Page with the given ID.

        The Notion API does not offer a DELETE method but insteads works by setting the `archived` field.
        """
        return self.update_database(page_id, {"archived": True})

    # ---------------------------------------------------------------------------
    # Pages
    # ---------------------------------------------------------------------------

    def get_page(self, page_id: Union[UUIDv4, str]) -> Page:
        "Get a single Notion page by its ID."
        response = self._make_request("get", f"pages/{page_id}")
        return Page(data=response).with_client(self)

    def create_page(self, page: Union[Page, dict]) -> Page:
        "Create a new Notion page."
        page_data = page.to_json() if isinstance(page, Page) else page
        response = self._make_request("post", "pages", page_data)
        return Page(data=response).with_client(self)

    def update_page(self, page_id: Union[UUIDv4, str], payload: dict) -> Page:
        "Update properties of an existing Notion page."
        response = self._make_request("patch", f"pages/{page_id}", payload)
        return Page(data=response).with_client(self)

    def delete_page(self, page_id: Union[UUIDv4, str]) -> Page:
        """Deletes the Notion Page with the given ID.

        The Notion API does not offer a DELETE method but insteads works by setting the `archived` field.
        """
        return self.update_page(page_id, {"archived": True})

    # ---------------------------------------------------------------------------
    # Blocks
    # ---------------------------------------------------------------------------

    def update_block(self, block_id: Union[UUIDv4, str], payload: dict):
        "Update properties of an existing Notion page."
        return self._make_request("patch", f"blocks/{block_id}", payload)

    def retrieve_block_children(
        self, block_id: Union[UUIDv4, str], limit: Optional[int] = None
    ):
        "Retrieve children of a given block."
        return self._make_request("get", f"blocks/{block_id}/children")

    def append_block_children(self, block_id: Union[UUIDv4, str], children: str):
        "Append children blocks to an existing block"
        return self._make_request(
            "patch", f"blocks/{block_id}/children", {"children": children}
        )

    def delete_block(self, block_id: Union[UUIDv4, str]):
        """Deletes the Notion Block with the given ID.

        The Notion API does not offer a DELETE method but insteads works by setting the `archived` field.
        """
        return self.update_block(block_id, {"archived": True})

    # ---------------------------------------------------------------------------
    # Comments
    # ---------------------------------------------------------------------------

    def get_comments(self, block_id: Union[UUIDv4, str]) -> List[Comment]:
        data = self._paginate("get", "comments", params={"block_id": block_id})
        return [
            Comment.from_json(comment_data).with_client(self) for comment_data in data
        ]

    def create_comment(self, comment: Comment) -> Comment:
        data = self._make_request(
            "post",
            "comments",
            payload=comment.to_json(),
        )
        return Comment.from_json(data)

    def delete_comment(self, comment_id: Union[UUIDv4, str]):
        raise NotImplementedError(
            "The Notion API does not allow deleting comments (yet)."
        )

    # ---------------------------------------------------------------------------
    # Search
    # ---------------------------------------------------------------------------

    def search(
        self,
        query: str,
        sort: dict = None,
        filter: Optional[dict] = None,
        limit: Optional[int] = None,
    ) -> List[Page]:
        "Search for Notion pages in all workspaces and databases."
        payload = {}  # type: Dict[str, Any]
        payload["query"] = query
        if sort:
            payload["sort"] = sort
        if filter:
            payload["filter"] = filter

        results = self._paginate("post", "search", payload, limit=limit)
        return [Page.from_json(page_data).with_client(self) for page_data in results]
