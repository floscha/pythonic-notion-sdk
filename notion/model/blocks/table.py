from typing import Optional, cast

from .block import Block
from .mixins import ChildrenMixin
from .table_row import TableRow


class Table(Block, ChildrenMixin):
    """A Notion Table block.

    See docs: https://developers.notion.com/reference/block#table-blocks
    """

    type = "table"

    def __init__(
        self,
        table_width: Optional[int] = None,
        has_column_header: Optional[bool] = False,
        has_row_header: Optional[bool] = False,
        children: Optional[list] = None,
    ):
        super().__init__()
        if children:
            assert all(isinstance(child, TableRow) for child in children)
        ChildrenMixin.__init__(self, children)

        self._data[self.type] |= {
            "table_width": table_width,
            "has_column_header": has_column_header,
            "has_row_header": has_row_header,
        }

    @property
    def rows(self) -> list[TableRow]:
        return cast(list[TableRow], self.children)

    @property
    def cells(self) -> list[list[str]]:
        return [row.cells for row in self.rows]
