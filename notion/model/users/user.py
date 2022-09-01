from typing import TYPE_CHECKING, TypeVar, Union

from notion.model.blocks import Block

if TYPE_CHECKING:
    from .bot import Bot
    from .person import Person


T = TypeVar("T")


class User(Block[T]):
    """Abstract Base Class for different User implementations.

    Docs: https://developers.notion.com/reference/user
    """

    type = "user"

    @property
    def name(self) -> str:
        return self._data["name"]

    @property
    def avatar_url(self) -> str:
        return self._data["avatar_url"]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, id={self.id})"

    @staticmethod
    def from_json(data) -> Union["Bot", "Person"]:  # type: ignore
        # Import at runtime to avoid circular imports.
        from notion.model.users import Bot, Person

        type_ = data.get("type")
        if type_ == "person":
            person = Person.__new__(Person)
            person._data = data
            return person
        elif type_ == "bot":
            bot = Bot.__new__(Bot)
            bot._data = data
            return bot
        else:
            raise ValueError(
                f"Type value of {type_} is (currently) not supported by Notion."
            )
