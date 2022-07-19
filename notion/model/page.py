from typing import Optional

from notion.model.block import ChildrenMixin
from notion.model.common import NotionObjectBase


def find_title_property_name(page: "Page") -> str:
    """Find the name of the title property for a page.

    While every page must have exactly one title, its name can be changed.
    """
    for property_name, property_dict in page._data["properties"].items():
        if property_dict["type"] == "title":
            return property_name


class TitleMixin:
    @property
    def title(self) -> str:
        title_property_name = find_title_property_name(self)
        return self._data["properties"][title_property_name]["title"][0]["plain_text"]

    @title.setter
    def title(self, new_title: str):
        title_property_name = find_title_property_name(self)
        new_data = self._client.update_page(
            self.id,
            {
                "properties": {
                    title_property_name: {"title": [{"text": {"content": new_title}}]}
                }
            },
        )
        self._data = new_data


class Page(NotionObjectBase, ChildrenMixin, TitleMixin):
    def __init__(
        self,
        title: str = None,
        title_property_name: str = "title",
        data=None,
        client=None,
    ):
        if title:
            data = {
                "object": "page",
                "properties": {
                    title_property_name: {"title": [{"text": {"content": title}}]},
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
