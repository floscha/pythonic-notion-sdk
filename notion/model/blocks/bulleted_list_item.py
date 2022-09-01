from typing import Optional

from notion.model.blocks import Block
from notion.model.blocks.mixins import ChildrenMixin, ColorMixin, RichTextMixin


class BulletedListItem(
    Block["BulletedListItem"], RichTextMixin, ColorMixin, ChildrenMixin
):
    """A Notion BulletedListItem block.

    See docs: https://developers.notion.com/reference/block#bulleted-list-item-blocks
    """

    type = "bulleted_list_item"

    def __init__(
        self, text: str, color: str = "default", children: Optional[list[Block]] = None
    ) -> None:
        super().__init__()
        RichTextMixin.__init__(self, text)
        ColorMixin.__init__(self, color)
        ChildrenMixin.__init__(self, children)
