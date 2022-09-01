from typing import TypeVar, Union

from notion.model.blocks import Block
from notion.model.properties.parent import ParentDatabase, ParentPage, ParentWorkspace

T = TypeVar("T")


class Child(Block[T]):
    "A block contained in another page."

    @property
    def title(self) -> str:
        return self._data[self.type]["title"]

    @property  # type: ignore
    def parent(self) -> Union[ParentWorkspace, ParentDatabase, ParentPage, None]:
        """Get the parent of the page.

        Since the ChildPage data itself does not contain the `parent` property, the full page must be retrieved first.
        """
        full_page = self._client.pages.get(self.id)
        return full_page.parent
