from typing import Optional

from notion.model.blocks import Block
from notion.model.blocks.mixins import ChildrenMixin, ColorMixin, RichTextMixin


class ToDo(Block, RichTextMixin, ColorMixin, ChildrenMixin):
    """A Notion ToDo block.

    See docs: https://developers.notion.com/reference/block#to-do-blocks
    """

    type = "to_do"

    def __init__(
        self,
        text: str,
        checked: bool = False,
        color: str = "default",
        children: Optional[list[Block]] = None,
    ):
        super().__init__()
        RichTextMixin.__init__(self, text)
        ColorMixin.__init__(self, color)
        ChildrenMixin.__init__(self, children)

        self._data[self.type] |= {"checked": checked}

    @property
    def checked(self) -> bool:
        return self._data[self.type]["checked"]

    @checked.setter
    def checked(self, new_checked: bool):
        new_data = self._client.blocks.update(
            self.id, {self.type: {"checked": new_checked}}
        )
        self._data = new_data

    def check(self):
        self.checked = True

    def uncheck(self):
        self.checked = False

    def toggle_check(self):
        if self.checked:
            self.uncheck()
        else:
            self.check()

    def check_all(self):
        """Checks an ToDo block and all of its children.

        Limitation: If the hierarchy is like ToDo -> BulletedListItem -> ToDo, the checking doesn't work.
        """
        self.check()
        for child in self.children:
            if isinstance(child, ToDo):
                child.check_all()

    def uncheck_all(self):
        """Unchecks an ToDo block and all of its children.

        Limitation: If the hierarchy is like ToDo -> BulletedListItem -> ToDo, the checking doesn't work.
        """
        self.uncheck()
        for child in self.children:
            if isinstance(child, ToDo):
                child.uncheck_all()
