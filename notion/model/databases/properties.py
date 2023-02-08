from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Union

from notion.model.properties.emoji import Emoji
from notion.model.properties.file import File
from notion.model.properties.rich_text import RichText
from notion.utils import JSON


class Property:
    @abstractmethod
    def to_json(self):
        raise NotImplementedError


class Title(Property):
    """Notion title property.

    Basically a list of RichText objects.

    Docs: https://developers.notion.com/reference/property-schema-object#title-configuration

    Each database must have exactly one database property schema object of type "title".
    This database property controls the title that appears at the top of the page when the page is opened.
    Title database property objects have no additional configuration within the title property.
    """

    def __init__(self, text: Union[RichText, str]) -> None:
        if isinstance(text, str):
            text = RichText(text)
        self.text = text

    @staticmethod
    def from_json(data: dict) -> "Title":
        return Title(data["title"][0]["text"]["content"])

    def to_json(self) -> List[dict]:
        return [self.text.to_json()]

    def __str__(self) -> str:
        return str(self.text)

    def __repr__(self) -> str:
        return str(self)


class Icon(Property):
    @staticmethod
    def from_str(icon: str) -> Union[Emoji, File]:
        if len(icon) == 1:  # Very simple heuristic to check if `icon` is an emoji.
            return Emoji(icon)
        else:  # Otherwise, assume an URL is provided.
            return File(icon)

    @staticmethod
    def from_json(data: dict) -> Union[Emoji, File]:
        icon_type = data["icon"]["type"]
        if icon_type == "emoji":
            return Emoji(data["icon"][icon_type])
        elif icon_type == "external":
            return File(data["icon"][icon_type])
        else:
            raise ValueError(f"Icon type {icon_type!r} is not supported.")


class Cover(Property):
    def __init__(self, url: str, type_: str = "external"):
        self.url = url
        self.type = type_

    @staticmethod
    def from_json(data: JSON) -> "Cover":
        assert isinstance(data, dict)
        type_ = data["type"]
        return Cover(type_, data[type_]["url"])

    def to_json(self) -> dict:
        return {"type": self.type, self.type: {"url": self.url}}


class Checkbox(Property):
    def __init__(self, checked: bool):
        self.checked = checked

    def to_json(self) -> dict:
        return {"type": "checkbox", "checkbox": self.checked}


SUPPORTED_COLORS = (
    "default",
    "gray",
    "brown",
    "orange",
    "yellow",
    "green",
    "blue",
    "purple",
    "pink",
    "red",
)


@dataclass
class SelectOption(Property):
    name: str
    color: str

    def __post_init__(self):
        if self.color not in SUPPORTED_COLORS:
            raise ValueError(f"Color {self.color!r} is not supported by Notion")

    def to_json(self):
        return {"name": self.name, "color": self.color}


@dataclass
class Select(Property):
    options: List[SelectOption]

    def to_json(self):
        return {"select": {"options": [option.to_json() for option in self.options]}}


class MultiSelect(Select):
    # TODO: Implement
    pass


class Number(Property):
    def __init__(self, format: str):
        self.format = format

    def to_json(self):
        return {"number": {"format": self.format}}


class Date(Property):
    def __init__(self, start: datetime, end: Optional[datetime] = None):
        self.start = start
        self.end = end

    def to_json(self):
        return {
            "date": {
                "start": self.start.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "end": self.end.strftime("%Y-%m-%dT%H:%M:%SZ"),
            }
        }


@dataclass
class Relation(Property):
    database_id: str
    type: str  # Can be "single_property" or "dual_property"

    def to_json(self):
        return {"relation": {"database_id": self.database_id, self.type: {}}}


@dataclass
class Rollup(Property):
    """.

    Params:
        function (str): The function that is evaluated for every page in the relation of the rollup.
                        Possible values include: count_all, count_values, count_unique_values, count_empty,
                        count_not_empty, percent_empty, percent_not_empty, sum, average, median, min, max, range, show_original
    """

    rollup_property_name: str
    relation_property_name: str
    function: Optional[str] = "count_all"

    def to_json(self):
        return {
            "rollup": {
                "rollup_property_name": self.rollup_property_name,
                "relation_property_name": self.relation_property_name,
                "function": self.function,
            }
        }


class People(Property):
    # TODO: Implement
    pass


class Files(Property):
    # TODO: Implement
    pass
