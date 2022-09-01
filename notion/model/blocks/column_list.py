from typing import Iterable

from .block import Block
from .column import Column
from .mixins import ChildrenMixin


class ColumnList(Block, ChildrenMixin):
    """A Notion ColumnList block.

    See docs: https://developers.notion.com/reference/block#column-list-and-column-blocks
    """

    type = "column_list"

    def __init__(
        self,
        children: list,
    ):
        super().__init__()
        assert all(isinstance(child, Column) for child in children)
        ChildrenMixin.__init__(self, children)

    def append_children(self, children):
        if not isinstance(children, Iterable):
            children = [children]

        if not all(isinstance(child, Column) for child in children):
            raise TypeError("ColumnLists can only have Column objects as children.")
        return super().append_children(children)

    def __getitem__(self, index: int) -> Column:
        column = self.children[index]
        assert isinstance(column, Column)
        return column
