from typing import Iterable, List, Optional, Type, Union

from notion.model.common.notion_object_base import BaseMixin, NotionObjectBase
from notion.model.common.parent import ParentDatabase, ParentPage, ParentWorkspace
from notion.model.common.utils import UUIDv4

# ---------------------------------------------------------------------------
# Base Class
# ---------------------------------------------------------------------------


class Block(NotionObjectBase):
    @property
    def type(self) -> str:
        return type_name_from_object(self)

    @property
    def has_children(self) -> bool:
        return self._data["has_children"]

    def delete(self):
        self._data = self._client.blocks.delete(self.id)

    def to_json(self) -> dict:
        res = self._data.copy()
        if "children" in res[self.type]:
            res[self.type]["children"] = [
                child.to_json() for child in res[self.type]["children"]
            ]
        return res


# ---------------------------------------------------------------------------
# Utils
# ---------------------------------------------------------------------------


def type_name_from_object(object) -> str:
    type_name = {
        ChildPage: "child_page",
        ChildDatabase: "child_database",
        Paragraph: "paragraph",
        HeadingOne: "heading_1",
        HeadingTwo: "heading_2",
        HeadingThree: "heading_3",
        Quote: "quote",
        Callout: "callout",
        Code: "code",
        Divider: "divider",
        Bookmark: "bookmark",
        Image: "image",
        BulletedListItem: "bulleted_list_item",
        NumberedListItem: "numbered_list_item",
        ToDo: "to_do",
        Toggle: "toggle",
        TableOfContents: "table_of_contents",
        Breadcrumb: "breadcrumb",
        Equation: "equation",
        Video: "video",
        File: "file",
        PDF: "pdf",
        LinkPreview: "link_preview",
        Embed: "embed",
        Template: "template",
        LinkToPage: "link_to_page",
        SyncedBlock: "synced_block",
        Column: "column",
        ColumnList: "column_list",
        Table: "table",
        TableRow: "table_row",
    }.get(type(object))
    if type_name is None:
        raise TypeError(f"Block type {str(type(object))!r} is not supported by Notion.")
    return type_name


def block_class_from_type_name(type_name: str) -> Type[Block]:
    type_class = {
        "child_page": ChildPage,
        "child_database": ChildDatabase,
        "paragraph": Paragraph,
        "heading_1": HeadingOne,
        "heading_2": HeadingTwo,
        "heading_3": HeadingThree,
        "quote": Quote,
        "callout": Callout,
        "code": Code,
        "divider": Divider,
        "bookmark": Bookmark,
        "image": Image,
        "bulleted_list_item": BulletedListItem,
        "numbered_list_item": NumberedListItem,
        "to_do": ToDo,
        "toggle": Toggle,
        "table_of_contents": TableOfContents,
        "breadcrumb": Breadcrumb,
        "equation": Equation,
        "video": Video,
        "file": File,
        "pdf": PDF,
        "link_preview": LinkPreview,
        "embed": Embed,
        "template": Template,
        "link_to_page": LinkToPage,
        "synced_block": SyncedBlock,
        "column": Column,
        "column_list": ColumnList,
        "table": Table,
        "table_row": TableRow,
    }.get(type_name)

    if type_class is None:
        raise TypeError(f"Block type {type_name!r} does not exist.")
    return type_class


# ---------------------------------------------------------------------------
# Mixins
# ---------------------------------------------------------------------------


class ChildrenMixin(BaseMixin):
    @property
    def children(self) -> list:
        return [
            block_class_from_type_name(data["type"])(client=self._client, data=data)
            for data in self._client.blocks.retrieve_children(self.id)["results"]
        ]

    def append_children(self, children) -> List[dict]:
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
                child._data["parent"] = {"type": "page_id", "page_id": self.id}
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


class RichTextMixin(BaseMixin):
    @property
    def text(self) -> str:
        return self._data[self.type]["rich_text"][0]["text"]["content"]

    @text.setter
    def text(self, new_text: str):
        new_data = self._client.blocks.update(
            self.id, {self.type: {"rich_text": [{"text": {"content": new_text}}]}}
        )
        self._data = new_data


class ColorMixin(BaseMixin):
    @property
    def color(self) -> str:
        return self._data[self.type]["color"]

    @color.setter
    def color(self, new_color: str):
        new_data = self._client.blocks.update(
            self.id, {self.type: {"color": new_color}}
        )
        self._data = new_data


class UrlMixin(BaseMixin):
    @property
    def url(self) -> str:
        return self._data[self.type]["url"]

    @url.setter
    def url(self, new_url: str):
        new_data = self._client.blocks.update(self.id, {self.type: {"url": new_url}})
        self._data = new_data


class CaptionMixin(BaseMixin):
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


class IconMixin(BaseMixin):
    @property
    def icon(self) -> Optional[str]:
        "TODO: Implement setter"
        icon_dict = self._data[self.type].get("icon")
        if icon_dict is None:
            return None
        elif "emoji" in icon_dict:
            return icon_dict["emoji"]
        else:
            raise NotImplementedError("`File Object` icons are not implemented yet.")

    @icon.setter
    def icon(self, new_icon: str):
        new_data = self._client.blocks.update(
            self.id, {self.type: {"icon": {"emoji": new_icon}}}
        )
        self._data = new_data


class ExternalFileMixin(BaseMixin):
    @property
    def url(self) -> str:
        return self._data[self.type]["external"]["url"]

    @url.setter
    def url(self, new_url: str):
        new_data = self._client.blocks.update(
            self.id, {self.type: {"external": {"url": new_url}}}
        )
        self._data = new_data


# ---------------------------------------------------------------------------
# Notion Block Implementations
# ---------------------------------------------------------------------------


class Child(Block):
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


class ChildPage(Child):
    """A page contained in another page.

    From the Notion docs (https://developers.notion.com/docs/working-with-page-content#modeling-content-as-blocks):
        When a child page appears inside another page, it's represented as a `child_page` block, which does not have children.
        You should think of this as a reference to the page block.
    """

    def delete(self):
        """Delete the `ChildPage` in Notion.

        Needs to be overwritten to use the `delete_page` endpoint instead of `delete_block`.
        """
        deletion_result = self._client.pages.delete(self.id)
        self._data["archived"] = deletion_result.archived


class ChildDatabase(Child):
    "A database contained in another page."

    def delete(self):
        """Delete the `ChildDatabase` in Notion.

        Needs to be overwritten to use the `delete_database` endpoint instead of `delete_block`.
        """
        deletion_result = self._client.databases.delete(self.id)
        self._data["archived"] = deletion_result["archived"]


class RichText(Block, RichTextMixin):
    def __init__(self, text: str = None, data=None, client=None) -> None:
        if not data:
            data = {
                "object": "block",
                "type": self.type,
                self.type: {"rich_text": [{"type": "text", "text": {"content": text}}]},
            }

        super().__init__(data, client)


class Paragraph(RichText):
    def __init__(self, text: str = None, data=None, client=None) -> None:
        super().__init__(text, data, client)


class HeadingOne(RichText):
    def __init__(self, text: str = None, data=None, client=None) -> None:
        super().__init__(text, data, client)


class HeadingTwo(RichText):
    def __init__(self, text: str = None, data=None, client=None) -> None:
        super().__init__(text, data, client)


class HeadingThree(RichText):
    def __init__(self, text: str = None, data=None, client=None) -> None:
        super().__init__(text, data, client)


class Quote(RichText):
    def __init__(self, text: str = None, data=None, client=None) -> None:
        super().__init__(text, data, client)


class Callout(RichText, IconMixin, ChildrenMixin, ColorMixin):
    """A Notion Callout block.

    See docs: https://developers.notion.com/reference/block#callout-blocks
    TODO: Add support for `File Object` icons.
    """

    def __init__(
        self,
        text: str = None,
        icon: str = None,
        color: str = "default",
        children: List[Block] = [],
        data: dict = None,
        client=None,
    ):
        if not data:
            data = {
                "object": "block",
                "type": self.type,
                self.type: {
                    "rich_text": [{"type": "text", "text": {"content": text}}],
                    "icon": {"emoji": icon} if icon else None,
                    "color": color,
                    "children": children,
                },
            }
        super().__init__(data=data, client=client)


CODE_BLOCK_LANGUAGES = [
    "abap",
    "arduino",
    "bash",
    "basic",
    "c",
    "clojure",
    "coffeescript",
    "c++",
    "c#",
    "css",
    "dart",
    "diff",
    "docker",
    "elixir",
    "elm",
    "erlang",
    "flow",
    "fortran",
    "f#",
    "gherkin",
    "glsl",
    "go",
    "graphql",
    "groovy",
    "haskell",
    "html",
    "java",
    "javascript",
    "json",
    "julia",
    "kotlin",
    "latex",
    "less",
    "lisp",
    "livescript",
    "lua",
    "makefile",
    "markdown",
    "markup",
    "matlab",
    "mermaid",
    "nix",
    "objective-c",
    "ocaml",
    "pascal",
    "perl",
    "php",
    "plain text",
    "powershell",
    "prolog",
    "protobuf",
    "python",
    "r",
    "reason",
    "ruby",
    "rust",
    "sass",
    "scala",
    "scheme",
    "scss",
    "shell",
    "sql",
    "swift",
    "typescript",
    "vb.net",
    "verilog",
    "vhdl",
    "visual basic",
    "webassembly",
    "xml",
    "yaml",
    "java/c/c++/c#",
]


class Code(RichText, CaptionMixin):
    """A Notion Code block.

    See docs: https://developers.notion.com/reference/block#code-blocks
    """

    @staticmethod
    def _check_language_is_valid(language: str):
        if language not in CODE_BLOCK_LANGUAGES:
            raise ValueError(
                f"Language {language!r} is not supported by Notion Code blocks."
            )

    def __init__(
        self,
        text: str = None,
        caption: str = None,
        language: str = "plain text",
        data: dict = None,
        client=None,
    ):
        Code._check_language_is_valid(language)

        if not data:
            data = {
                "object": "block",
                "type": self.type,
                self.type: {
                    "rich_text": [{"type": "text", "text": {"content": text}}],
                    "language": language,
                },
            }
            if caption is not None:
                data[self.type]["caption"] = [
                    {"type": "text", "text": {"content": caption}}
                ]

        super().__init__(data=data, client=client)

    @property
    def language(self) -> str:
        return self._data[self.type]["language"]

    @language.setter
    def language(self, new_language: str):
        Code._check_language_is_valid(new_language)

        new_data = self._client.blocks.update(
            self.id, {self.type: {"language": new_language}}
        )
        self._data = new_data


class Divider(Block):
    def __init__(self, data: dict = None, client=None):
        if not data:
            data = {
                "object": "block",
                "type": self.type,
                self.type: {},
            }

        super().__init__(data=data, client=client)


class Bookmark(Block, UrlMixin, CaptionMixin):
    def __init__(
        self, url: str = None, caption: str = None, data: dict = None, client=None
    ):
        if not data:
            caption_data = [{"text": {"content": caption}}] if caption else []
            data = {
                "object": "block",
                "type": self.type,
                self.type: {"url": url, "caption": caption_data},
            }

        super().__init__(data=data, client=client)


class Image(Block, ExternalFileMixin):
    """A Notion Image block.

    See docs: https://developers.notion.com/reference/block#image-blocks
    """

    def __init__(self, url: str = None, data: dict = None, client=None):
        if not data:
            data = {
                "object": "block",
                "type": self.type,
                self.type: {"external": {"url": url}},
            }

        super().__init__(data=data, client=client)


class BulletedListItem(Block, RichTextMixin, ColorMixin, ChildrenMixin):
    """A Notion BulletedListItem block.

    See docs: https://developers.notion.com/reference/block#bulleted-list-item-blocks
    """

    def __init__(
        self, text: str = None, color: str = "default", data: dict = None, client=None
    ):
        if not data:
            data = {
                "object": "block",
                "type": self.type,
                self.type: {
                    "rich_text": [{"type": "text", "text": {"content": text}}],
                    "color": color,
                },
            }

        super().__init__(data=data, client=client)


class NumberedListItem(Block, RichTextMixin, ColorMixin, ChildrenMixin):
    """A Notion NumberedListItem block.

    See docs: https://developers.notion.com/reference/block#numbered-list-item-blocks
    """

    def __init__(
        self, text: str = None, color: str = "default", data: dict = None, client=None
    ):
        if not data:
            data = {
                "object": "block",
                "type": self.type,
                self.type: {
                    "rich_text": [{"type": "text", "text": {"content": text}}],
                    "color": color,
                },
            }

        super().__init__(data=data, client=client)


class ToDo(Block, RichTextMixin, ColorMixin, ChildrenMixin):
    """A Notion ToDo block.

    See docs: https://developers.notion.com/reference/block#to-do-blocks
    """

    def __init__(
        self,
        text: str = None,
        checked: bool = False,
        color: str = "default",
        data: dict = None,
        client=None,
    ):
        if not data:
            data = {
                "object": "block",
                "type": self.type,
                self.type: {
                    "rich_text": [{"type": "text", "text": {"content": text}}],
                    "checked": checked,
                    "color": color,
                },
            }

        super().__init__(data=data, client=client)

    @property
    def checked(self) -> bool:
        return self._data[self.type]["checked"]

    @checked.setter
    def checked(self, new_checked: bool):
        new_data = self._client.blocks.update(
            self.id, {self.type: {"checked": new_checked}}
        )
        self._data = new_data

    def check(self):
        self.checked = True

    def uncheck(self):
        self.checked = False

    def toggle_check(self):
        if self.checked:
            self.uncheck()
        else:
            self.check()

    def check_all(self):
        """Checks an ToDo block and all of its children.

        Limitation: If the hierarchy is like ToDo -> BulletedListItem -> ToDo, the checking doesn't work.
        """
        self.check()
        for child in self.children:
            if isinstance(child, ToDo):
                child.check_all()

    def uncheck_all(self):
        """Unchecks an ToDo block and all of its children.

        Limitation: If the hierarchy is like ToDo -> BulletedListItem -> ToDo, the checking doesn't work.
        """
        self.uncheck()
        for child in self.children:
            if isinstance(child, ToDo):
                child.uncheck_all()


class Toggle(Block, RichTextMixin, ColorMixin, ChildrenMixin):
    """A Notion Toggle block.

    See docs: https://developers.notion.com/reference/block#toggle-blocks
    """

    def __init__(
        self,
        text: str = None,
        color: str = "default",
        data: dict = None,
        client=None,
    ):
        if not data:
            data = {
                "object": "block",
                "type": self.type,
                self.type: {
                    "rich_text": [{"type": "text", "text": {"content": text}}],
                    "color": color,
                },
            }

        super().__init__(data=data, client=client)


class TableOfContents(Block, ColorMixin):

    """A Notion Table Of Contents block.

    See docs: https://developers.notion.com/reference/block#table-of-contents-blocks
    """

    def __init__(
        self,
        color: str = "default",
        data: dict = None,
        client=None,
    ):
        if not data:
            data = {
                "object": "block",
                "type": self.type,
                self.type: {
                    "color": color,
                },
            }

        super().__init__(data=data, client=client)


class Breadcrumb(Block):

    """A Notion Breadcrumb block.

    See docs: https://developers.notion.com/reference/block#breadcrumb-blocks
    """

    def __init__(
        self,
        data: dict = None,
        client=None,
    ):
        if not data:
            data = {
                "object": "block",
                "type": self.type,
                self.type: {},
            }

        super().__init__(data=data, client=client)


class Equation(Block):
    """A Notion Equation block.

    See docs: https://developers.notion.com/reference/block#equation-blocks
    """

    def __init__(
        self,
        expression: str = None,
        data: dict = None,
        client=None,
    ):
        if not data:
            data = {
                "object": "block",
                "type": self.type,
                self.type: {"expression": expression},
            }

        super().__init__(data=data, client=client)

    @property
    def expression(self) -> str:
        return self._data[self.type]["expression"]

    @expression.setter
    def expression(self, new_expression: str):
        new_data = self._client.blocks.update(
            self.id, {self.type: {"expression": new_expression}}
        )
        self._data = new_data


class Video(Block, ExternalFileMixin):
    """A Notion Video block.

    See docs: https://developers.notion.com/reference/block#video-blocks
    """

    def __init__(self, url: str = None, data: dict = None, client=None):
        if not data:
            data = {
                "object": "block",
                "type": self.type,
                self.type: {"external": {"url": url}},
            }

        super().__init__(data=data, client=client)


class File(Block, ExternalFileMixin, CaptionMixin):
    """A Notion File block.

    See docs: https://developers.notion.com/reference/block#file-blocks
    """

    def __init__(
        self, url: str = None, caption: str = None, data: dict = None, client=None
    ):
        if not data:
            caption_data = [{"text": {"content": caption}}] if caption else []
            data = {
                "object": "block",
                "type": self.type,
                self.type: {"external": {"url": url}, "caption": caption_data},
            }

        super().__init__(data=data, client=client)


class PDF(Block, ExternalFileMixin):
    """A Notion PDF block.

    See docs: https://developers.notion.com/reference/block#pdf-blocks
    """

    def __init__(self, url: str = None, data: dict = None, client=None):
        if not data:
            data = {
                "object": "block",
                "type": self.type,
                self.type: {"external": {"url": url}},
            }

        super().__init__(data=data, client=client)


class LinkPreview(Block, UrlMixin):
    """A Notion LinkPreview block.

    NOTE: The link_preview block will only be returned as part of a response. It cannot be created via the API.
    See docs: https://developers.notion.com/reference/block#link-preview-blocks
    """

    def __init__(self, data: dict = None, client=None):
        super().__init__(data=data, client=client)

    @UrlMixin.url.setter  # type: ignore
    def url(self, new_url):
        raise TypeError(
            "LinkPreview blocks will only be returned as part of a response. It cannot be created via the API."
        )


class Embed(Block, UrlMixin):
    """A Notion Embed block.

    See docs: https://developers.notion.com/reference/block#embed-blocks
    """

    def __init__(self, url: str = None, data: dict = None, client=None):
        if not data:
            data = {
                "object": "block",
                "type": self.type,
                self.type: {"url": url},
            }

        super().__init__(data=data, client=client)


class Template(Block, RichTextMixin, ChildrenMixin):
    """A Notion Template block.

    See docs: https://developers.notion.com/reference/block#template-blocks
    """

    def __init__(self, text: str = None, data: dict = None, client=None):
        if not data:
            data = {
                "object": "block",
                "type": self.type,
                self.type: {
                    "rich_text": [{"type": "text", "text": {"content": text}}],
                },
            }

        super().__init__(data=data, client=client)


class LinkToPage(Block):
    """A Notion LinkToPage block.

    NOTE: Once created, the `page_id` and `database_id` parameters are currently read-only.

    See docs: https://developers.notion.com/reference/block#link-to-page-blocks
    """

    def __init__(
        self,
        page_id: Optional[UUIDv4] = None,
        database_id: Optional[UUIDv4] = None,
        data: dict = None,
        client=None,
    ):
        if not data:
            if not (page_id or database_id):
                raise ValueError("Either `page_id` or `database_id` must be set.")
            if page_id and database_id:
                raise ValueError("Only one of `page_id` and `database_id` can be set.")

            data = {
                "object": "block",
                "type": self.type,
                self.type: {},
            }
            if page_id:
                data[self.type]["type"] = "page_id"
                data[self.type]["page_id"] = page_id
            if database_id:
                data[self.type]["type"] = "database_id"
                data[self.type]["database_id"] = database_id

        super().__init__(data=data, client=client)

    @property
    def page_id(self) -> UUIDv4:
        return self._data[self.type].get("page_id")

    @property
    def database_id(self) -> UUIDv4:
        return self._data[self.type].get("database_id")


class SyncedBlock(Block, ChildrenMixin):
    """A Notion SyncedBlock block.

    Similar to the UI, there are two versions of a SyncedBlock:
    1. The original block that was created first and doesn't yet sync with anything else.
    2. The reference blocks that are synced to the original synced block.

    See docs: https://developers.notion.com/reference/block#synced-block-blocks
    """

    def __init__(
        self,
        synced_from: Optional[UUIDv4] = None,
        data: dict = None,
        client=None,
    ):
        if not data:
            data = {
                "object": "block",
                "type": self.type,
                self.type: {"synced_from": {}},
            }
            if synced_from:
                data[self.type]["synced_from"] = {"block_id": synced_from}
            else:
                data[self.type]["synced_from"] = None

        super().__init__(data=data, client=client)

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


class Column(Block, ChildrenMixin):
    """A Notion Column block.

    See docs: https://developers.notion.com/reference/block#column-list-and-column-blocks
    """

    def __init__(
        self,
        children: Optional[List[Block]] = None,
        data: dict = None,
        client=None,
    ):
        if not data:
            assert isinstance(children, list)
            data = {
                "object": "block",
                "type": self.type,
                self.type: {"children": children},
            }
        super().__init__(data=data, client=client)


class ColumnList(Block, ChildrenMixin):
    """A Notion ColumnList block.

    See docs: https://developers.notion.com/reference/block#column-list-and-column-blocks
    """

    def __init__(
        self,
        children: Optional[List[Column]] = None,
        data: dict = None,
        client=None,
    ):
        if not data:
            assert isinstance(children, list)
            data = {
                "object": "block",
                "type": self.type,
                self.type: {"children": children},
            }
        super().__init__(data=data, client=client)

    def append_children(self, children):
        if not isinstance(children, Iterable):
            children = [children]

        if not all(isinstance(child, Column) for child in children):
            raise TypeError("ColumnLists can only have Column objects as children.")
        return super().append_children(children)

    def __getitem__(self, index: int) -> Column:
        return self.children[index]


class TableRow(Block):
    """A Notion TableRow block.

    See docs: https://developers.notion.com/reference/block#table-row-blocks
    """

    def __init__(
        self,
        cells: Optional[List] = None,
        data: dict = None,
        client=None,
    ):
        if not data:
            assert isinstance(cells, list)
            data = {
                "object": "block",
                "type": self.type,
                self.type: {
                    "cells": [
                        [{"type": "text", "text": {"content": cell_text}}]
                        for cell_text in cells
                    ]
                },
            }
        super().__init__(data=data, client=client)

    @property
    def cells(self) -> List[str]:
        return [c[0]["text"]["content"] for c in self._data[self.type]["cells"]]


class Table(Block, ChildrenMixin):
    """A Notion Table block.

    See docs: https://developers.notion.com/reference/block#table-blocks
    """

    def __init__(
        self,
        table_width: Optional[int] = None,
        has_column_header: Optional[bool] = False,
        has_row_header: Optional[bool] = False,
        children: Optional[List[Column]] = None,
        data: dict = None,
        client=None,
    ):
        if not data:
            assert isinstance(children, list)
            data = {
                "object": "block",
                "type": self.type,
                self.type: {
                    "table_width": table_width,
                    "has_column_header": has_column_header,
                    "has_row_header": has_row_header,
                    "children": children,
                },
            }
        super().__init__(data=data, client=client)

    @property
    def rows(self) -> List[TableRow]:
        return self.children

    @property
    def cells(self) -> List[List[str]]:
        return [row.cells for row in self.rows]
