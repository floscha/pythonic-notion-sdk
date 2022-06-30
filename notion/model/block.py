from notion.model.common import NotionObjectBase

from typing import List, Union


class Block(NotionObjectBase):
    @property
    def type(self) -> str:
        return self._data["type"]

    @property
    def has_children(self) -> bool:
        return self._data["has_children"]

    def delete(self):
        self._client.delete_block(self.id)


class ChildPage(Block):
    """A page contained in another page.

    From the Notion docs (https://developers.notion.com/docs/working-with-page-content#modeling-content-as-blocks):
        When a child page appears inside another page, it's represented as a `child_page` block, which does not have children.
        You should think of this as a reference to the page block.
    """

    @property
    def title(self) -> str:
        return self._data["child_page"]["title"]

    @property
    def parent(self):
        """Get the parent of the page.

        Since the ChildPage data itself does not contain the `parent` property, the full page must be retrieved first.
        """
        full_page = self._client.get_page(self.id)
        return full_page.parent

    def delete(self):
        """Delete the ChildPage.

        Needs to be overwritten to use the `delete_page` endpoint instead of `delete_block`.
        """
        self._client.delete_page(self.id)


def block_class_from_type_name(type_name: str) -> Block:
    type_class = {
        "child_page": ChildPage,
        "paragraph": Paragraph,
        "heading_1": Heading,
        "heading_2": SubHeading,
        "heading_3": SubSubHeading,
        "quote": Quote,
    }.get(type_name)

    if type_class is None:
        raise TypeError(f"Block type {type_name!r} does not exist.")
    return type_class


class ChildrenMixin:
    @property
    def children(self) -> list:
        return [
            block_class_from_type_name(data["type"])(client=self._client, data=data)
            for data in self._client.retrieve_block_children(self.id)["results"]
        ]

    def append_children(self, children: Union[dict, List[dict]]):
        """Append blocks or pages to a parent.

        TODO: Instead of appending items one by one, batch blocks to be more efficient.
        """
        if not isinstance(children, list):
            children = [children]
        children = [c._data for c in children]

        res = []
        for c in children:
            object_name = c["object"]
            if object_name == "block":
                res.extend(self._client.append_block_children(self.id, [c]))
            elif object_name == "page":
                # TODO Also support database_id
                c["parent"] = {"type": "page_id", "page_id": self.id}
                res.append(self._client.create_page(c))
            else:
                raise TypeError(
                    f"Appending objects of type {object_name} is not supported."
                )

        return res


class RichText(Block):
    def __init__(
        self, class_name: str = None, text: str = None, data=None, client=None
    ) -> None:
        if class_name and text:
            data = {
                "object": "block",
                "type": class_name,
                class_name: {
                    "rich_text": [{"type": "text", "text": {"content": text}}]
                },
            }

        super().__init__(data, client)

    @property
    def text(self) -> str:
        return self._data[self.type]["rich_text"][0]["text"]["content"]

    @text.setter
    def text(self, new_text: str):
        new_data = self._client.update_block(
            self.id, {self.type: {"rich_text": [{"text": {"content": new_text}}]}}
        )
        self._data = new_data


class Paragraph(RichText):
    def __init__(self, text: str = None, data=None, client=None) -> None:
        super().__init__("paragraph", text, data, client)


class Heading(RichText):
    def __init__(self, text: str = None, data=None, client=None) -> None:
        super().__init__("heading_1", text, data, client)


class SubHeading(RichText):
    def __init__(self, text: str = None, data=None, client=None) -> None:
        super().__init__("heading_2", text, data, client)


class SubSubHeading(RichText):
    def __init__(self, text: str = None, data=None, client=None) -> None:
        super().__init__("heading_3", text, data, client)


class Quote(RichText):
    def __init__(self, text: str = None, data=None, client=None) -> None:
        super().__init__("quote", text, data, client)
