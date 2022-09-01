from typing import Optional, Type, cast

from notion.model import blocks

from .base_mixin import BaseMixin


def block_class_from_type_name(type_name: str) -> Type[blocks.Block]:
    type_class = {
        "child_page": blocks.ChildPage,
        "child_database": blocks.ChildDatabase,
        "paragraph": blocks.Paragraph,
        "heading_1": blocks.HeadingOne,
        "heading_2": blocks.HeadingTwo,
        "heading_3": blocks.HeadingThree,
        "quote": blocks.Quote,
        "callout": blocks.Callout,
        "code": blocks.Code,
        "divider": blocks.Divider,
        "bookmark": blocks.Bookmark,
        "image": blocks.Image,
        "bulleted_list_item": blocks.BulletedListItem,
        "numbered_list_item": blocks.NumberedListItem,
        "to_do": blocks.ToDo,
        "toggle": blocks.Toggle,
        "table_of_contents": blocks.TableOfContents,
        "breadcrumb": blocks.Breadcrumb,
        "equation": blocks.Equation,
        "video": blocks.Video,
        "file": blocks.File,
        "pdf": blocks.PDF,
        "link_preview": blocks.LinkPreview,
        "embed": blocks.Embed,
        "template": blocks.Template,
        "link_to_page": blocks.LinkToPage,
        "synced_block": blocks.SyncedBlock,
        "column": blocks.Column,
        "column_list": blocks.ColumnList,
        "table": blocks.Table,
        "table_row": blocks.TableRow,
    }.get(type_name)

    if type_class is None:
        raise TypeError(f"Block type {type_name!r} does not exist.")
    return cast(Type[blocks.Block], type_class)


class ChildrenMixin(BaseMixin):
    def __init__(self, children: Optional[list[blocks.Block]] = None):
        if children is not None:
            if self.type == "page":
                self._data["children"] = [child.to_json() for child in children]
            else:
                self._data[self.type]["children"] = [
                    child.to_json() for child in children
                ]

    @property
    def children(self) -> list[blocks.Block]:
        children_data = self._client.blocks.retrieve_children(self.id)
        return [
            block_class_from_type_name(data["type"])
            .from_json(data)
            .with_client(self._client)
            for data in children_data
        ]

    def append_children(self, children) -> list[dict]:
        """Append blocks or pages to a parent.

        TODO: Instead of appending items one by one, batch blocks to be more efficient.
        """
        if not isinstance(children, list):
            children = [children]

        res = []
        for child in children:
            object_name = child._data["object"]
            if object_name == "block":
                append_results = self._client.blocks.append_children(
                    self.id, [child.to_json()]
                )
                new_block = append_results["results"][0]
                child._data = new_block
                child._client = self._client
                res.append(new_block)
            elif object_name == "page":
                # TODO Also support database_id
                child._data["parent"] = {"page_id": self.id}
                res.append(self._client.pages.create(child._data))
            else:
                raise TypeError(
                    f"Appending objects of type {object_name} is not supported."
                )

        return res

    def delete(self):
        # Apparently all children must be deleted first, before the block itself can be deleted.
        for child in self.children:
            child.delete()

        super().delete()
