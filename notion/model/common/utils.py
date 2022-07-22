import re
from datetime import datetime


def is_valid_notion_id(id_str: str) -> bool:
    id_regex = r"^[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12}$"
    match = re.search(id_regex, id_str)
    return bool(match)


def parse_notion_datetime(datetime_str: str) -> datetime:
    "Turn a Notion datetime string into a Python `datetime` object."
    return datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%f%z")


class UUIDv4(str):
    def __new__(cls, value):
        if not is_valid_notion_id(value):
            raise ValueError(f"{value!r} is not a valid Notion ID.")

        return str.__new__(cls, value)


def class_name_as_snake_case(class_: object) -> str:
    """Returns the class name of an object as a snake case string.

    Regex taken from StackOverflow:
        https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
    """
    return re.sub(r"(?<!^)(?=[A-Z])", "_", type(class_).__name__).lower()
