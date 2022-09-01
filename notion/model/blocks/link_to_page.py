from typing import Optional

from notion.model.properties.uuidv4 import UUIDv4

from .block import Block


class LinkToPage(Block["LinkToPage"]):
    """A Notion LinkToPage block.

    NOTE: Once created, the `page_id` and `database_id` parameters are currently read-only.

    See docs: https://developers.notion.com/reference/block#link-to-page-blocks
    """

    type = "link_to_page"

    def __init__(
        self,
        page_id: Optional[UUIDv4] = None,
        database_id: Optional[UUIDv4] = None,
    ):
        super().__init__()

        if not (page_id or database_id):
            raise ValueError("Either `page_id` or `database_id` must be set.")
        if page_id and database_id:
            raise ValueError("Only one of `page_id` and `database_id` can be set.")

        if page_id:
            self._data[self.type] |= {"type": "page_id"}
            self._data[self.type] |= {"page_id": page_id}
        if database_id:
            self._data[self.type] |= {"type": "database_id"}
            self._data[self.type] |= {"database_id": database_id}

    @property
    def page_id(self) -> UUIDv4:
        return self._data[self.type].get("page_id")

    @property
    def database_id(self) -> UUIDv4:
        return self._data[self.type].get("database_id")
