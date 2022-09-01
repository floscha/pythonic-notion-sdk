from .block import Block
from .mixins import ColorMixin


class TableOfContents(Block, ColorMixin):

    """A Notion Table Of Contents block.

    See docs: https://developers.notion.com/reference/block#table-of-contents-blocks
    """

    type = "table_of_contents"

    def __init__(
        self,
        color: str = "default",
    ):

        super().__init__()
        ColorMixin.__init__(self, color)
