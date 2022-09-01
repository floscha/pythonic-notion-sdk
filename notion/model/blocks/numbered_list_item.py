from typing import Optional

from .block import Block
from .mixins import ChildrenMixin, ColorMixin, RichTextMixin


class NumberedListItem(
    Block["NumberedListItem"], RichTextMixin, ColorMixin, ChildrenMixin
):
    """A Notion NumberedListItem block.

    See docs: https://developers.notion.com/reference/block#numbered-list-item-blocks
    """

    type = "numbered_list_item"

    def __init__(
        self, text: str, color: str = "default", children: Optional[list[Block]] = None
    ) -> None:
        super().__init__()
        RichTextMixin.__init__(self, text)
        ColorMixin.__init__(self, color)
        ChildrenMixin.__init__(self, children)
