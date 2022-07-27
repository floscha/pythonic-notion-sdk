from typing import Dict, Optional, Union

from notion.model.block import ChildrenMixin
from notion.model.common.notion_object_base import NotionObjectBase
from notion.model.databases.properties import Property


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
        properties: Optional[Dict[str, Union[Property, dict]]] = None,
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
        if properties:
            for property_name, property in properties.items():
                if isinstance(property, Property):
                    property = property.to_json()
                data["properties"][property_name] = property

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
    def url(self) -> str:
        return self._data["url"]

    def delete(self):
        if self._client is None:
            raise Exception(
                "Page has not been created in Notion yet and therefore cannot be deleted."
            )
        else:
            new_data = self._client.delete_page(self.id)
            self._data = new_data

    @staticmethod
    def from_json(data: dict) -> "Page":
        new_page = Page()
        new_page._data = data
        return new_page

    def to_json(self) -> dict:
        return self._data.copy()

    def __str__(self) -> str:
        return f"Page(Title: {self.title!r}, ID: {self.id!r})"

    def __repr__(self) -> str:
        return str(self)
