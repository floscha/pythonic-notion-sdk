from typing import Optional

from notion.model.properties.uuidv4 import UUIDv4

from .block import Block
from .mixins import ChildrenMixin


class SyncedBlock(Block, ChildrenMixin):
    """A Notion SyncedBlock block.

    Similar to the UI, there are two versions of a SyncedBlock:
    1. The original block that was created first and doesn't yet sync with anything else.
    2. The reference blocks that are synced to the original synced block.

    See docs: https://developers.notion.com/reference/block#synced-block-blocks
    """

    type = "synced_block"

    def __init__(
        self,
        synced_from: Optional[UUIDv4] = None,
    ):
        super().__init__()
        ChildrenMixin.__init__(self)

        self._data[self.type] |= {
            "synced_from": {"block_id": synced_from} if synced_from else None
        }

    @property
    def synced_from(self) -> Optional[UUIDv4]:
        synced_from_dict = self._data[self.type]["synced_from"]
        if synced_from_dict:
            return synced_from_dict["block_id"]
        else:
            return None

    def append_children(self, children):
        if self.synced_from is not None:
            raise TypeError("Only Original SyncedBlocks can hold children.")
        return super().append_children(children)
