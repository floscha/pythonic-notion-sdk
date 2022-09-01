import re


def is_valid_notion_id(id_str: str) -> bool:
    id_regex = r"^[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12}$"
    match = re.search(id_regex, id_str)
    return bool(match)


class UUIDv4(str):
    def __new__(cls, value):
        if not is_valid_notion_id(value):
            raise ValueError(f"{value!r} is not a valid Notion ID.")

        return str.__new__(cls, value)
