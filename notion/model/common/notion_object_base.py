from datetime import datetime
from typing import Union

from notion.model.common.parent import Parent, ParentPage
from notion.model.common.utils import parse_notion_datetime


class NotionObjectBase:
    def __init__(self, data=None, client=None):
        self._data = data
        self._client = client

    def with_client(self, client) -> "NotionObjectBase":
        self._client = client
        return self

    @property
    def object(self) -> str:
        """Get the Notion object type of the page as a string.

        Takes the value from the page's data while in practice it must always be `"page"`.
        """
        return self._data["object"]

    @property
    def id(self) -> str:
        return self._data["id"]

    @property
    def parent(self) -> Parent:
        return Parent.from_json(self._data)

    @parent.setter
    def parent(self, new_parent: Union[ParentPage, str]):
        if isinstance(new_parent, str):
            new_parent = ParentPage(new_parent)

        self._data["parent"] = new_parent.to_json()

    @property
    def created_time(self) -> datetime:
        return parse_notion_datetime(self._data["created_time"])

    @property
    def created_by(self) -> dict:
        """Get the user that created the page/block.

        Example: {"object": "user", "id": "45ee8d13-687b-47ce-a5ca-6e2e45548c4b"}
        """
        return self._data["created_by"]

    @property
    def last_edited_time(self) -> datetime:
        return parse_notion_datetime(self._data["last_edited_time"])

    @property
    def last_edited_by(self) -> dict:
        return self._data["created_by"]

    @property
    def archived(self) -> bool:
        return self._data["archived"]
