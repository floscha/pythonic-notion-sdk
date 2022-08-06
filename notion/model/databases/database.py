from typing import Any, Dict, List, Optional, Union

import notion.model.databases.properties as props
from notion.model.common.notion_object_base import NotionObjectBase
from notion.model.common.parent import ParentDatabase, ParentPage
from notion.model.databases.properties import Cover, Icon, Title
from notion.model.filters import Filter
from notion.model.page import Page


def property_class_to_str_or_dict(property_class):
    if isinstance(property_class, type):
        class_name = {
            props.Title: "title",
            props.RichText: "rich_text",
            props.Checkbox: "checkbox",
            props.Date: "date",
            props.Files: "files",
            props.People: "people",
        }[property_class]
        return {class_name: {}}
    else:
        return property_class.to_json()


class Database(NotionObjectBase):
    """Notion Database

    Params:
        title (optional): If not provided, Notion will set the title to `Untitled`.
    """

    def __init__(
        self,
        title: Optional[str] = None,
        icon: Optional[Union[Icon, str]] = None,
        cover: Optional[Union[Cover, str]] = None,
        properties: Optional[Dict[str, Any]] = None,
        parent: Optional[Union[ParentPage, str]] = None,
    ):
        self._client = None

        self._data = {
            "object": "database",
            "properties": {
                "Name": {"title": {}},
            },
        }
        if title:
            self.title = title
        if icon:
            self.icon = icon
        if cover:
            self.cover = cover
        if properties:
            for property_name, property_class in properties.items():
                property_class_repr = property_class_to_str_or_dict(property_class)
                if property_class_repr is None:
                    print(f"Property type {property_class!r} is not supported (yet).")
                    continue
                self._data["properties"][property_name] = property_class_repr
        if parent:
            self.parent = parent

        super().__init__(self._data, None)

    @staticmethod
    def from_json(data: dict) -> "Database":
        new_database = Database()
        new_database._data = data
        return new_database

    def create(self, client, parent: str = None) -> "Database":
        client.create_database(self, parent)
        self._client = client
        return self

    def __add__(self, page: Page) -> "Database":
        if page.parent:
            raise Exception("Page parent is already set.")
        page.parent = ParentDatabase(self.id)
        self._client.create_page(page)
        return self

    def query(
        self, filter_: Union[Filter, dict], sort: Optional[dict] = None
    ) -> List[Page]:
        """Query database for specific pages.

        _filter should be a `Filter` object, but can also be dict for more flexibility.
        """
        if not self._client:
            raise Exception(
                "Database has not been created. Run `your_database.create(...)` first."
            )
        return self._client.query_database(self.id, filter_, sort)

    def delete(self):
        if self._client is None:
            raise Exception(
                "Database has not been created in Notion yet and therefore cannot be deleted."
            )
        else:
            new_data = self._client.delete_database(self.id)
            self._data = new_data

    @property
    def title(self) -> Title:
        return Title.from_json(self._data)

    @title.setter
    def title(self, new_title: Union[Title, str]):
        if isinstance(new_title, str):
            new_title = Title(new_title)

        if self._client is None:
            self._data["title"] = new_title.to_json()
        else:
            new_data = self._client.update_database(
                self.id, {"title": new_title.to_json()}
            )
            self._data = new_data

    @property
    def icon(self) -> Icon:
        return Icon.from_json(self._data)

    @icon.setter
    def icon(self, new_icon: Union[Icon, str]):
        if isinstance(new_icon, str):
            new_icon = Icon.from_str(new_icon)

        if self._client is None:
            self._data["icon"] = new_icon.to_json()
        else:
            new_data = self._client.update_database(
                self.id, {"icon": new_icon.to_json()}
            )
            self._data = new_data

    @property
    def cover(self) -> Cover:
        return Cover.from_json(self._data)

    @cover.setter
    def cover(self, new_cover: Union[Cover, str]):
        if isinstance(new_cover, str):
            new_cover = Cover(new_cover)

        if self._client is None:
            self._data["cover"] = new_cover.to_json()
        else:
            new_data = self._client.update_database(
                self.id, {"cover": new_cover.to_json()}
            )
            self._data = new_data
