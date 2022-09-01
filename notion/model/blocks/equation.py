from .block import Block


class Equation(Block["Equation"]):
    """A Notion Equation block.

    See docs: https://developers.notion.com/reference/block#equation-blocks
    """

    type = "equation"

    def __init__(self, expression: str = None):
        super().__init__()
        self._data[self.type] |= {"expression": expression}

    @property
    def expression(self) -> str:
        return self._data[self.type]["expression"]

    @expression.setter
    def expression(self, new_expression: str):
        new_data = self._client.blocks.update(
            self.id, {self.type: {"expression": new_expression}}
        )
        self._data = new_data
