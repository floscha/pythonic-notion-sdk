from .block import Block
from .mixins import RichTextMixin


class Quote(Block["Quote"], RichTextMixin):
    type = "quote"

    def __init__(self, text: str) -> None:
        super().__init__()
        RichTextMixin.__init__(self, text)
