from typing import Any, Dict, List, Optional, Union

import requests

from notion.api import endpoints
from notion.utils import JSON

API_BASE_URL = "https://api.notion.com/v1/"
API_VERSION = "2022-06-28"


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
        self.blocks = endpoints.BlocksEndpoint(self)
        self.comments = endpoints.CommentsEndpoint(self)
        self.databases = endpoints.DatabasesEndpoint(self)
        self.pages = endpoints.PagesEndpoint(self)
        self.search = endpoints.SearchEndpoint(self)
        self.users = endpoints.UsersEndpoint(self)

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
