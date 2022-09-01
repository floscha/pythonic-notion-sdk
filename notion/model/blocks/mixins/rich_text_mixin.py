from .base_mixin import BaseMixin


class RichTextMixin(BaseMixin):
    def __init__(self, text: str):
        self._data[self.type] |= {
            "rich_text": [{"type": "text", "text": {"content": text}}]
        }

    @property
    def text(self) -> str:
        return self._data[self.type]["rich_text"][0]["text"]["content"]

    @text.setter
    def text(self, new_text: str):
        new_data = self._client.blocks.update(
            self.id, {self.type: {"rich_text": [{"text": {"content": new_text}}]}}
        )
        self._data = new_data
