from typing import Optional

from notion.model.blocks import Block
from notion.model.blocks.mixins.rich_text_mixin import RichTextMixin
from notion.model.blocks.mixins.toggleable_mixin import ToggleableMixin


class HeadingOne(Block["HeadingOne"], RichTextMixin, ToggleableMixin):
    type = "heading_1"

    def __init__(self, text: str, toggleable: Optional[bool] = False) -> None:
        super().__init__()
        RichTextMixin.__init__(self, text)
        ToggleableMixin.__init__(self, toggleable)


class HeadingTwo(Block["HeadingTwo"], RichTextMixin, ToggleableMixin):
    type = "heading_2"

    def __init__(self, text: str, toggleable: Optional[bool] = False) -> None:
        super().__init__()
        RichTextMixin.__init__(self, text)
        ToggleableMixin.__init__(self, toggleable)


class HeadingThree(Block["HeadingThree"], RichTextMixin, ToggleableMixin):
    type = "heading_3"

    def __init__(self, text: str, toggleable: Optional[bool] = False) -> None:
        super().__init__()
        RichTextMixin.__init__(self, text)
        ToggleableMixin.__init__(self, toggleable)
