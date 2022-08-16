from notion.model.common import NotionObjectBase
from notion.model.common.types import JSON


class Comment(NotionObjectBase):
    def __init__(self, parent=None, text=None):
        self._data = {
            "parent": {"page_id": parent},
            "rich_text": [{"text": {"content": text}}],
        }

    @staticmethod
    def from_json(data: JSON):
        new_comment = Comment()
        new_comment._data = data
        return new_comment

    def to_json(self) -> JSON:
        return self._data

    @property
    def text(self):
        "FIXME Is there a text mixin?!"
        return self._data["rich_text"][0]["text"]["content"]
