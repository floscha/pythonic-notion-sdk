from .block import Block
from .mixins import CaptionMixin, RichTextMixin

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


def check_language_is_valid(language: str):
    if language not in CODE_BLOCK_LANGUAGES:
        raise ValueError(
            f"Language {language!r} is not supported by Notion Code blocks."
        )


class Code(Block["Code"], RichTextMixin, CaptionMixin):
    """A Notion Code block.

    See docs: https://developers.notion.com/reference/block#code-blocks
    """

    type = "code"

    def __init__(
        self,
        text: str,
        language: str = "plain text",
        caption: str = None,
    ):
        check_language_is_valid(language)

        super().__init__()
        RichTextMixin.__init__(self, text)
        CaptionMixin.__init__(self, caption)

        self._data[self.type] |= {"language": language}

    @property
    def language(self) -> str:
        return self._data[self.type]["language"]

    @language.setter
    def language(self, new_language: str):
        check_language_is_valid(new_language)

        new_data = self._client.blocks.update(
            self.id, {self.type: {"language": new_language}}
        )
        self._data = new_data
