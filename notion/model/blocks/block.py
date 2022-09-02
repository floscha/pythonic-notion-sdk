from abc import ABC, abstractproperty
from datetime import datetime
from typing import TYPE_CHECKING, Generic, TypeVar, Union, cast

from notion.logger import logger
from notion.model.properties.parent import (
    Parent,
    ParentDatabase,
    ParentPage,
    ParentWorkspace,
)
from notion.utils import parse_notion_datetime

if TYPE_CHECKING:
    from notion.api.client import NotionClient

T = TypeVar("T")


class Block(Generic[T], ABC):
    def __init__(self):
        self._data = {"object": "block", "type": self.type, self.type: {}}
        self._client = None

    @classmethod
    def from_json(cls, data: dict) -> T:
        obj = cls.__new__(cls)
        obj._data = data
        return cast(T, obj)

    def to_json(self) -> dict:
        res = self._data.copy()
        if self.type != "page" and "children" in res[self.type]:
            res[self.type]["children"] = [
                child.to_json() if isinstance(child, Block) else child
                for child in res[self.type]["children"]
            ]
        return res

    def with_client(self, client: "NotionClient") -> T:
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

        if self._client:
            logger.warning(
                "Changes to the `parent` property can currently not be updated using the Notion API."
            )

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

    @abstractproperty
    def type(self) -> str:
        raise NotImplementedError

    @property
    def has_children(self) -> bool:
        return self._data["has_children"]

    def delete(self):
        self._data = self._client.blocks.delete(self.id)
