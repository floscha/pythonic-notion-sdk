from notion.model.blocks import Block
from notion.model.blocks.mixins import UrlMixin


class LinkPreview(Block["LinkPreview"], UrlMixin):
    """A Notion LinkPreview block.

    NOTE: The link_preview block will only be returned as part of a response. It cannot be created via the API.
    See docs: https://developers.notion.com/reference/block#link-preview-blocks
    """

    type = "link_preview"

    def __init__(self, url: str):
        super().__init__()
        UrlMixin.__init__(self, url)

    @property
    def url(self) -> str:
        return self.url

    @url.setter
    def url(self, _):
        raise TypeError(
            "LinkPreview blocks will only be returned as part of a response. It cannot be created via the API."
        )
