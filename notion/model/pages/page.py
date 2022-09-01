from typing import Dict, Optional, Union

from notion.model.blocks import Block
from notion.model.blocks.mixins import ChildrenMixin, TitleMixin
from notion.model.databases.properties import Property


class Page(Block["Page"], ChildrenMixin, TitleMixin):
    type = "page"

    def __init__(
        self,
        title: str,
        properties: Optional[Dict[str, Union[Property, dict]]] = None,
    ):
        super().__init__()
        ChildrenMixin.__init__(self, [])

        # Page needs no "page" property.
        del self._data["page"]

        self._data["object"] = "page"
        self._data["properties"] = {
            "title": {"title": [{"text": {"content": title}}]},
        }

        if properties:
            for property_name, property in properties.items():
                if isinstance(property, Property):
                    property = property.to_json()
                self._data["properties"][property_name] = property

    def create(self, client, parent: str = None) -> "Page":
        client.pages.create(self, parent)
        self._client = client
        return self

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

    def __str__(self) -> str:
        return f"Page(Title: {self.title!r}, ID: {self.id!r})"

    def __repr__(self) -> str:
        return str(self)