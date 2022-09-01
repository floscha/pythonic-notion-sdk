import re
from datetime import datetime
from typing import Union

JSON = Union[dict, list]


def parse_notion_datetime(datetime_str: str) -> datetime:
    "Turn a Notion datetime string into a Python `datetime` object."
    return datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%f%z")


def class_name_as_snake_case(class_: object) -> str:
    """Returns the class name of an object as a snake case string.

    Regex taken from StackOverflow:
        https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
    """
    return re.sub(r"(?<!^)(?=[A-Z])", "_", type(class_).__name__).lower()
