from .block import Block
from .mixins import ExternalFileMixin


class Image(Block, ExternalFileMixin):
    """A Notion Image block.

    See docs: https://developers.notion.com/reference/block#image-blocks
    """

    type = "image"

    def __init__(self, url: str):
        super().__init__()
        ExternalFileMixin.__init__(self, url)
