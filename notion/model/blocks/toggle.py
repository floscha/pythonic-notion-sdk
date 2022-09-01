from notion.model.blocks import Block
from notion.model.blocks.mixins import ChildrenMixin, ColorMixin, RichTextMixin


class Toggle(Block, RichTextMixin, ColorMixin, ChildrenMixin):
    """A Notion Toggle block.

    See docs: https://developers.notion.com/reference/block#toggle-blocks
    """

    type = "toggle"

    def __init__(
        self,
        text: str,
        color: str = "default",
    ):
        super().__init__()
        RichTextMixin.__init__(self, text)
        ColorMixin.__init__(self, color)
        ChildrenMixin.__init__(self)
