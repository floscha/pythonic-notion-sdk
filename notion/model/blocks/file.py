from notion.model.blocks import Block
from notion.model.blocks.mixins import CaptionMixin, ExternalFileMixin


class File(Block, ExternalFileMixin, CaptionMixin):
    """A Notion File block.

    See docs: https://developers.notion.com/reference/block#file-blocks
    """

    type = "file"

    def __init__(self, url: str, caption: str = None):
        super().__init__()
        ExternalFileMixin.__init__(self, url)
        CaptionMixin.__init__(self, caption)
