from typing import TYPE_CHECKING, Any, Dict, List, Optional

from notion.model import Page

if TYPE_CHECKING:
    from notion.api.client import NotionClient


class SearchEndpoint:
    def __init__(self, client: "NotionClient"):
        self._client = client

    def __call__(
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

        results = self._client._paginate("post", "search", payload, limit=limit)
        return [
            Page.from_json(page_data).with_client(self._client) for page_data in results
        ]
