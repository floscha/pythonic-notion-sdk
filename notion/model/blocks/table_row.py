from typing import Optional

from notion.model.blocks import Block


class TableRow(Block["TableRow"]):
    """A Notion TableRow block.

    See docs: https://developers.notion.com/reference/block#table-row-blocks
    """

    type = "table_row"

    def __init__(
        self,
        cells: Optional[list] = None,
    ):
        super().__init__()

        assert isinstance(cells, list)
        self._data[self.type] |= {
            "cells": [
                [{"type": "text", "text": {"content": cell_text}}]
                for cell_text in cells
            ]
        }

    @property
    def cells(self) -> list[str]:
        return [c[0]["text"]["content"] for c in self._data[self.type]["cells"]]
