from .block import Block
from .mixins import ExternalFileMixin


class PDF(Block, ExternalFileMixin):
    """A Notion PDF block.

    See docs: https://developers.notion.com/reference/block#pdf-blocks
    """

    type = "pdf"

    def __init__(self, url: str):
        super().__init__()
        ExternalFileMixin.__init__(self, url)
