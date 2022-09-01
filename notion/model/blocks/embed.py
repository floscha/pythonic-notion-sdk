from .block import Block
from .mixins import UrlMixin


class Embed(Block, UrlMixin):
    """A Notion Embed block.

    See docs: https://developers.notion.com/reference/block#embed-blocks
    """

    type = "embed"

    def __init__(self, url: str):
        super().__init__()
        UrlMixin.__init__(self, url)
