from notion.model.block import *


def test_all_blocks_are_implemented():
    """Assert that all blocks from the API docs are implemented.

    Reference: https://developers.notion.com/reference/block#block-type-object
    """
    Paragraph
    HeadingOne
    HeadingTwo
    HeadingThree
    Callout
    Quote
    BulletedListItem
    NumberedListItem
    ToDo
    Toggle
    Code
    ChildPage
    ChildDatabase
    Embed
    Image
    Video
    File
    PDF
    Bookmark
    Equation
    Divider
    TableOfContents
    Breadcrumb
    ColumnList
    Column
    LinkPreview
    Template
    LinkToPage
    SyncedBlock
    Table
    TableRow
