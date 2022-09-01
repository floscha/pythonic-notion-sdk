from notion.model.blocks import Block
from notion.model.blocks.mixins import ExternalFileMixin


class Video(Block["Video"], ExternalFileMixin):
    """A Notion Video block.

    See docs: https://developers.notion.com/reference/block#video-blocks
    """

    type = "video"

    def __init__(self, url: str):
        super().__init__()
        ExternalFileMixin.__init__(self, url)
