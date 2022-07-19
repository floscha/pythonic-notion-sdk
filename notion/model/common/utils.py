import re
from datetime import datetime


def is_valid_notion_id(id_str: str) -> bool:
    id_regex = r"^[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12}$"
    match = re.search(id_regex, id_str)
    return bool(match)


def parse_notion_datetime(datetime_str: str) -> datetime:
    "Turn a Notion datetime string into a Python `datetime` object."
    return datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%f%z")
