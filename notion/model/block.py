from typing import List, Optional, Union

from notion.model.common import NotionObjectBase


def type_name_from_object(object) -> str:
    type_name = {
        ChildPage: "child_page",
        Paragraph: "paragraph",
        Heading: "heading_1",
        SubHeading: "heading_2",
        SubSubHeading: "heading_3",
        Quote: "quote",
        Callout: "callout",
        Code: "code",
        Divider: "divider",
        Bookmark: "bookmark",
        Image: "image",
    }.get(type(object))
    if type_name is None:
        raise TypeError(f"Block type {str(type(object))!r} is not supported by Notion.")
    return type_name


class Block(NotionObjectBase):
    @property
    def type(self) -> str:
        return type_name_from_object(self)

    @property
    def has_children(self) -> bool:
        return self._data["has_children"]

    def delete(self):
        self._data = self._client.delete_block(self.id)


class ChildPage(Block):
    """A page contained in another page.

    From the Notion docs (https://developers.notion.com/docs/working-with-page-content#modeling-content-as-blocks):
        When a child page appears inside another page, it's represented as a `child_page` block, which does not have children.
        You should think of this as a reference to the page block.
    """

    @property
    def title(self) -> str:
        # return self._data["child_page"]["title"]
        return self._data[self.type]["title"]

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
        deletion_result = self._client.delete_page(self.id)
        self._data["archived"] = deletion_result["archived"]


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

        res = []
        for child in children:
            c = child._data
            object_name = c["object"]
            if object_name == "block":
                append_results = self._client.append_block_children(self.id, [c])
                new_block = append_results["results"][0]
                child._data = new_block
                child._client = self._client
                res.append(new_block)
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
    def __init__(self, text: str = None, data=None, client=None) -> None:
        if not data:
            data = {
                "object": "block",
                "type": self.type,
                self.type: {"rich_text": [{"type": "text", "text": {"content": text}}]},
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
        super().__init__(text, data, client)


class Heading(RichText):
    def __init__(self, text: str = None, data=None, client=None) -> None:
        super().__init__(text, data, client)


class SubHeading(RichText):
    def __init__(self, text: str = None, data=None, client=None) -> None:
        super().__init__(text, data, client)


class SubSubHeading(RichText):
    def __init__(self, text: str = None, data=None, client=None) -> None:
        super().__init__(text, data, client)


class Quote(RichText):
    def __init__(self, text: str = None, data=None, client=None) -> None:
        super().__init__(text, data, client)


class Callout(RichText, ChildrenMixin):
    """A Notion Callout block.

    See docs: https://developers.notion.com/reference/block#callout-blocks
    TODO: Add support for `File Object` icons.
    """

    def __init__(
        self,
        text: str = None,
        icon: str = None,
        color: str = "default",
        children: List[Block] = None,
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
                    "children": [block._data for block in children] if children else [],
                },
            }
        super().__init__(data=data, client=client)

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
        new_data = self._client.update_block(
            self.id, {self.type: {"icon": {"emoji": new_icon}}}
        )
        self._data = new_data

    @property
    def color(self) -> str:
        return self._data[self.type]["color"]

    @color.setter
    def color(self, new_color: str):
        new_data = self._client.update_block(self.id, {self.type: {"color": new_color}})
        self._data = new_data


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


class Code(RichText):
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
    def caption(self) -> str:
        return self._data[self.type]["caption"]

    @caption.setter
    def caption(self, new_caption: str):

        new_data = self._client.update_block(
            self.id, {self.type: {"rich_text": [{"text": {"content": new_caption}}]}}
        )
        self._data = new_data

    @property
    def language(self) -> str:
        return self._data[self.type]["language"]

    @language.setter
    def language(self, new_language: str) -> str:
        Code._check_language_is_valid(new_language)

        new_data = self._client.update_block(
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


class Bookmark(Block):
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

    @property
    def url(self) -> str:
        return self._data[self.type]["url"]

    @url.setter
    def url(self, new_url: str) -> str:
        new_data = self._client.update_block(self.id, {self.type: {"url": new_url}})
        self._data = new_data

    @property
    def caption(self) -> str:
        caption_data = self._data[self.type]["caption"]
        if not caption_data:
            return None

        return caption_data[0]["text"]["content"]

    @caption.setter
    def caption(self, new_caption: str):
        new_data = self._client.update_block(
            self.id, {self.type: {"caption": [{"text": {"content": new_caption}}]}}
        )
        self._data = new_data


class Image(Block):
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

    @property
    def url(self) -> str:
        return self._data[self.type]["external"]["url"]

    @url.setter
    def url(self, new_url: str) -> str:
        new_data = self._client.update_block(
            self.id, {self.type: {"external": {"url": new_url}}}
        )
        self._data = new_data
