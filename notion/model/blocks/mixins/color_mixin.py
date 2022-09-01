from .base_mixin import BaseMixin


class ColorMixin(BaseMixin):
    def __init__(self, color: str):
        self._data[self.type] |= {"color": color}

    @property
    def color(self) -> str:
        return self._data[self.type]["color"]

    @color.setter
    def color(self, new_color: str):
        new_data = self._client.blocks.update(
            self.id, {self.type: {"color": new_color}}
        )
        self._data = new_data
