from notion.model.blocks import Block


class Breadcrumb(Block["Breadcrumb"]):
    """A Notion Breadcrumb block.

    See docs: https://developers.notion.com/reference/block#breadcrumb-blocks
    """

    type = "breadcrumb"

    def __init__(self) -> None:
        super().__init__()
