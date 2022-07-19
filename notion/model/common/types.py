from notion.model.common.utils import is_valid_notion_id
from notion.model.common.utils import is_valid_notion_id


class UUIDv4(str):
    def __init__(self, str_):
        if not is_valid_notion_id(str_):
            raise ValueError(f"{str_!r} is not a valid Notion ID.")

        super(str_)
