from typing import Optional

from .base_mixin import BaseMixin


class ToggleableMixin(BaseMixin):
    def __init__(self, toggleable: Optional[bool] = False):
        self._data[self.type] |= {"is_toggleable": toggleable}

    @property
    def is_toggleable(self) -> bool:
        return self._data[self.type]["is_toggleable"]

    @is_toggleable.setter
    def is_toggleable(self, toggleable: bool):
        new_data = self._client.blocks.update(
            self.id,
            {
                self.type: {
                    "is_toggleable": toggleable,
                    # Update requires a "rich_text" field, so include the old value.
                    # Will hopefully be fixed in the future. Until then typing must be ignored.
                    "rich_text": [{"text": {"content": self.text}}],  # type: ignore
                }
            },
        )
        self._data = new_data
