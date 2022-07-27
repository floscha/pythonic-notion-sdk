from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Union

from notion.model.common.emoji import Emoji
from notion.model.common.file import File
from notion.model.common.rich_text import RichText


class Property:
    pass


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

    def to_json(self) -> dict:
        return [self.text.to_json()]

    def __str__(self) -> str:
        return str(self.text)

    def __repr__(self) -> str:
        return str(self)


class Icon:
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


class Cover:
    def __init__(self, url: str, type_: str = "external"):
        self.url = url
        self.type = type_

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
class SelectOption:
    name: str
    color: str

    def __post_init__(self):
        if self.color not in SUPPORTED_COLORS:
            raise ValueError(f"Color {self.color!r} is not supported by Notion")

    def to_json(self):
        return {"name": self.name, "color": self.color}


@dataclass
class Select:
    options: List[SelectOption]

    def to_json(self):
        return {"select": {"options": [option.to_json() for option in self.options]}}


class MultiSelect(Select):
    pass


class Number:
    def __init__(self, format: str):
        self.format = format

    def to_json(self):
        return {"number": {"format": self.format}}


class Date(datetime):
    pass


@dataclass
class Relation:
    database_id: str
    type: str  # Can be "single_property" or "dual_property"

    def to_json(self):
        return {"relation": {"database_id": self.database_id, self.type: {}}}


@dataclass
class Rollup:
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


class People:
    pass


class Files:
    pass
