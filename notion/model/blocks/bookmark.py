from typing import Optional

from notion.model.blocks import Block
from notion.model.blocks.mixins import CaptionMixin, UrlMixin


class Bookmark(Block["Bookmark"], UrlMixin, CaptionMixin):
    type = "bookmark"

    def __init__(self, url: str, caption: Optional[str] = None) -> None:
        super().__init__()
        UrlMixin.__init__(self, url)
        CaptionMixin.__init__(self, caption)
