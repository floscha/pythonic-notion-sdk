from typing import TYPE_CHECKING, TypeVar, Union

from notion.model.common import NotionObjectBase

if TYPE_CHECKING:
    from .bot import Bot
    from .person import Person


T = TypeVar("T")


class User(NotionObjectBase[T]):
    """Abstract Base Class for different User implementations.

    Docs: https://developers.notion.com/reference/user
    """

    @property
    def type(self) -> str:
        return self._data["type"]

    @property
    def name(self) -> str:
        return self._data["name"]

    @property
    def avatar_url(self) -> str:
        return self._data["avatar_url"]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, id={self.id})"

    @staticmethod
    def from_json(data) -> Union["Bot", "Person"]:
        # Import at runtime to avoid circular imports.
        from notion.model.users import Bot, Person

        type_ = data.get("type")
        if type_ == "person":
            return Person.from_json(data)
        elif type_ == "bot":
            return Bot.from_json(data)
        else:
            raise ValueError(
                f"Type value of {type_} is (currently) not supported by Notion."
            )
