from typing import Optional, Union

from .base_mixin import BaseMixin


class CaptionMixin(BaseMixin):
    def __init__(self, caption: Optional[str] = None):
        if caption:
            self._data[self.type] |= {"caption": [{"text": {"content": caption}}]}

    @property
    def caption(self) -> Union[str, None]:
        caption_data = self._data[self.type]["caption"]
        if not caption_data:
            return None

        return caption_data[0]["text"]["content"]

    @caption.setter
    def caption(self, new_caption: str):
        new_data = self._client.blocks.update(
            self.id, {self.type: {"caption": [{"text": {"content": new_caption}}]}}
        )
        self._data = new_data
