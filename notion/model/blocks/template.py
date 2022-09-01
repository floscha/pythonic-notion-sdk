from notion.model.blocks import Block
from notion.model.blocks.mixins import ChildrenMixin, RichTextMixin


class Template(Block, RichTextMixin, ChildrenMixin):
    """A Notion Template block.

    See docs: https://developers.notion.com/reference/block#template-blocks
    """

    type = "template"

    def __init__(self, text: str):
        super().__init__()
        RichTextMixin.__init__(self, text)
        ChildrenMixin.__init__(self)
