from .block import Block
from .mixins.rich_text_mixin import RichTextMixin


class Paragraph(Block["Paragraph"], RichTextMixin):
    type = "paragraph"

    def __init__(self, text: str) -> None:
        super().__init__()
        RichTextMixin.__init__(self, text)
