from typing import Optional

from notion.model.block import ChildrenMixin
from notion.model.common import NotionObjectBase


class TitleMixin:
    @property
    def title(self) -> str:
        return self._data["properties"]["title"]["title"][0]["plain_text"]

    @title.setter
    def title(self, new_title: str):
        new_data = self._client.update_page(
            self.id,
            {"properties": {"title": {"title": [{"text": {"content": new_title}}]}}},
        )
        self._data = new_data


class Page(NotionObjectBase, ChildrenMixin, TitleMixin):
    def __init__(self, title: str = None, data=None, client=None):
        if title:
            data = {
                "object": "page",
                "properties": {
                    "title": {"title": [{"text": {"content": title}}]},
                },
            }
        super().__init__(data, client)

    @property
    def icon(self) -> Optional[dict]:
        return self._data["icon"]

    @property
    def cover(self) -> Optional[dict]:
        return self._data["cover"]

    @property
    def properties(self) -> dict:
        return self._data["properties"]

    @property
    def parent(self) -> dict:
        "Get the parent of the page."
        return self._data["parent"]

    @property
    def url(self) -> str:
        return self._data["url"]

    def delete(self):
        self._client.delete_page(self.id)
