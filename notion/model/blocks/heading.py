from notion.model.blocks import Block
from notion.model.blocks.mixins.rich_text_mixin import RichTextMixin


class HeadingOne(Block["HeadingOne"], RichTextMixin):
    type = "heading_1"

    def __init__(self, text: str) -> None:
        super().__init__()
        RichTextMixin.__init__(self, text)


class HeadingTwo(Block["HeadingTwo"], RichTextMixin):
    type = "heading_2"

    def __init__(self, text: str) -> None:
        super().__init__()
        RichTextMixin.__init__(self, text)


class HeadingThree(Block["HeadingThree"], RichTextMixin):
    type = "heading_3"

    def __init__(self, text: str) -> None:
        super().__init__()
        RichTextMixin.__init__(self, text)
