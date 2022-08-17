from abc import ABC
from datetime import datetime
from typing import Any, Generic, TypeVar, Union, cast

from notion.model.common.parent import (
    Parent,
    ParentDatabase,
    ParentPage,
    ParentWorkspace,
)
from notion.model.common.utils import parse_notion_datetime


class BaseMixin(ABC):
    _client: Any
    _data: Any

    @property
    def type(self):
        raise NotImplementedError

    @property
    def id(self):
        raise NotImplementedError


T = TypeVar("T")


class NotionObjectBase(Generic[T]):
    def __init__(self, data=None, client=None):
        self._data = data
        self._client = client

    def with_client(self, client) -> T:
        self._client = client
        return cast(T, self)

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
    def parent(self) -> Union[ParentWorkspace, ParentPage, ParentDatabase, None]:
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
