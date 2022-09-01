from typing import Optional

from notion.model.blocks import Block
from notion.model.blocks.mixins import ChildrenMixin


class Column(Block["Column"], ChildrenMixin):
    """A Notion Column block.

    See docs: https://developers.notion.com/reference/block#column-list-and-column-blocks
    """

    type = "column"

    def __init__(
        self,
        children: Optional[list[Block]] = None,
    ):
        super().__init__()
        ChildrenMixin.__init__(self, children)
