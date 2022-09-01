from notion.model.blocks import Block
from notion.model.blocks.mixins import (
    ChildrenMixin,
    ColorMixin,
    IconMixin,
    RichTextMixin,
)


class Callout(Block["Callout"], RichTextMixin, IconMixin, ColorMixin, ChildrenMixin):
    """A Notion Callout block.

    See docs: https://developers.notion.com/reference/block#callout-blocks
    TODO: Add support for `File Object` icons.
    """

    type = "callout"

    def __init__(
        self,
        text: str,
        icon: str,
        color: str = "default",
        children: list[Block] = None,
    ):
        super().__init__()
        RichTextMixin.__init__(self, text)
        IconMixin.__init__(self, icon)
        ColorMixin.__init__(self, color)
        ChildrenMixin.__init__(self, children)
