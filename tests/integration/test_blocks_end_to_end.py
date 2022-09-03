from datetime import datetime, timezone
from os import environ

from pydotenvs import load_env
from pytest import fixture

from notion import NotionClient
from notion.model import blocks
from notion.model.pages import Page
from notion.model.properties.colors import Colors
from notion.model.properties.parent import ParentPage, ParentWorkspace
from notion.model.properties.uuidv4 import is_valid_notion_id

load_env()
TEST_NOTION_TOKEN = environ["TEST_NOTION_TOKEN"]
TEST_NOTION_PAGE = environ["TEST_NOTION_PAGE"]


@fixture
def client() -> NotionClient:
    return NotionClient(TEST_NOTION_TOKEN)


@fixture
def page(client: NotionClient) -> Page:
    return client.pages.get(TEST_NOTION_PAGE)


def test_creating_client(client):
    "Simply check if a Notion client can be created."
    assert isinstance(client, NotionClient)


def test_getting_test_page(page):
    "Check if the test page can be retrieved and has the correct title."
    assert page.title == "pythonic-notion-playground"


def test_page_has_correct_properties(page):
    """Check if the test page has all the correct properties.

    Compare to https://developers.notion.com/reference/page
    """
    assert page.object == "page"
    assert page.id == TEST_NOTION_PAGE
    assert page.created_time == datetime(2022, 6, 24, 9, 8, 0, 0, tzinfo=timezone.utc)
    created_by_dict = page.created_by
    assert created_by_dict["object"] == "user"
    assert is_valid_notion_id(created_by_dict["id"])
    # Exact datetime cannot be determined since every test run edits the page...
    assert page.last_edited_time.tzinfo == timezone.utc
    last_edited_by_dict = page.last_edited_by
    assert last_edited_by_dict["object"] == "user"
    assert is_valid_notion_id(last_edited_by_dict["id"])
    assert page.archived == False
    assert page.icon == None
    assert page.cover == None
    assert list(page.properties.keys()) == ["title"]
    assert page.url == f"https://www.notion.so/{page.title}-{page.id.replace('-', '')}"


def test_page_has_no_children(page: Page):
    "At the beginning of the integration tests, the page should have no children."
    assert page.children == []


def test_adding_children(page: Page):
    """Test adding various blocks and pages as children.

    Especially validate that adding a list of BOTH blocks and pages works, as the official API
    supports adding a list of block only.
    """
    page.append_children(
        [
            blocks.HeadingOne("Heading 1"),
            blocks.HeadingTwo("Heading 2"),
            blocks.HeadingThree("Heading 3"),
            blocks.Paragraph("Some Text"),
            Page("Sub Page"),
            blocks.Quote("Some Quote"),
        ]
    )

    all_children = page.children
    for child, type_ in zip(
        all_children,
        ("heading_1", "heading_2", "heading_3", "paragraph", "child_page", "quote"),
    ):
        assert is_valid_notion_id(child.id)
        assert child.object == "block"
        assert child.type == type_


def test_heading_1_block_has_correct_properties(page):
    """Check if the test block has all the correct properties.

    Compare to https://developers.notion.com/reference/block
    """
    heading_1_block = page.children[0]
    assert heading_1_block.object == "block"
    assert is_valid_notion_id(heading_1_block.id)
    assert heading_1_block.type == "heading_1"
    # Exact datetime cannot be determined since every test run re-creates the block...
    assert heading_1_block.created_time.tzinfo == timezone.utc
    created_by_dict = heading_1_block.created_by
    assert created_by_dict["object"] == "user"
    assert is_valid_notion_id(created_by_dict["id"])
    # Exact datetime cannot be determined since every test run re-creates the block...
    assert heading_1_block.last_edited_time.tzinfo == timezone.utc
    last_edited_by_dict = heading_1_block.last_edited_by
    assert last_edited_by_dict["object"] == "user"
    assert is_valid_notion_id(last_edited_by_dict["id"])
    assert heading_1_block.archived == False
    assert heading_1_block.has_children == False


def test_toggleable_heading_blocks(page: Page):
    headings = [
        blocks.HeadingOne("Non-toggleable Heading 1"),
        blocks.HeadingTwo("Non-toggleable Heading 2"),
        blocks.HeadingThree("Non-toggleable Heading 3"),
    ]
    page.append_children(headings)

    for current_heading in headings:
        assert current_heading.is_toggleable == False

    for current_heading in headings:
        current_heading.is_toggleable = True
        assert current_heading.is_toggleable == True

    for current_heading in headings:
        current_heading.delete()
        assert current_heading.archived == True


def test_callout_block(page):
    callout = blocks.Callout(
        "Some Text", "⭐", Colors.green, children=[blocks.Quote("Some Quote")]
    )
    page.append_children(callout)

    assert is_valid_notion_id(callout.id)
    assert callout.text == "Some Text"
    assert callout.icon == "⭐"
    assert callout.color == "green"
    assert callout.has_children == True

    callout.color = "red_background"
    callout.icon = "🔥"
    assert callout.color == "red_background"
    assert callout.icon == "🔥"

    callout.delete()
    assert callout.archived == True


def test_code_block(page: Page):
    code = blocks.Code("print('Hello World')")
    page.append_children(code)

    assert is_valid_notion_id(code.id)
    assert code.text == "print('Hello World')"
    assert code.language == "plain text"

    code.language = "python"
    assert code.language == "python"

    code.delete()
    assert code.archived == True


def test_divider_block(page: Page):
    divider = blocks.Divider()
    page.append_children(divider)

    assert is_valid_notion_id(divider.id)

    divider.delete()
    assert divider.archived == True


def test_bookmark_block(page: Page):
    bookmark = blocks.Bookmark(url="https://www.notion.so")
    page.append_children(bookmark)

    assert is_valid_notion_id(bookmark.id)
    assert bookmark.url == "https://www.notion.so"
    assert bookmark.caption is None

    bookmark.url = "https://www.notion.so/blog"
    bookmark.caption = "The Notion Blog"
    assert bookmark.url == "https://www.notion.so/blog"
    assert bookmark.caption == "The Notion Blog"

    bookmark.delete()
    assert bookmark.archived == True


def test_image_block(page: Page):
    image = blocks.Image("https://super.so/icon/dark/image.svg")
    page.append_children(image)

    assert is_valid_notion_id(image.id)
    assert image.url == "https://super.so/icon/dark/image.svg"

    image.url = "https://super.so/icon/dark/home.svg"
    assert image.url == "https://super.so/icon/dark/home.svg"

    image.delete()
    assert image.archived == True


def test_bulleted_list_item_block(page: Page):
    bulleted_list = blocks.BulletedListItem("Item B")
    page.append_children(bulleted_list)

    assert is_valid_notion_id(bulleted_list.id)
    assert bulleted_list.text == "Item B"

    bulleted_list.text = "Item A"
    assert bulleted_list.text == "Item A"

    bulleted_list.append_children(
        [blocks.BulletedListItem("Item a"), blocks.BulletedListItem("Item b")]
    )
    assert [child.text for child in bulleted_list.children] == ["Item a", "Item b"]

    bulleted_list.delete()
    assert bulleted_list.archived == True


def test_numbered_list_item_block(page: Page):
    numbered_list = blocks.NumberedListItem("Item B")
    page.append_children(numbered_list)

    assert is_valid_notion_id(numbered_list.id)
    assert numbered_list.text == "Item B"

    numbered_list.text = "Item A"
    assert numbered_list.text == "Item A"

    numbered_list.append_children(
        [blocks.NumberedListItem("Item a"), blocks.NumberedListItem("Item b")]
    )
    assert [child.text for child in numbered_list.children] == ["Item a", "Item b"]

    numbered_list.delete()
    assert numbered_list.archived == True


def test_to_do_block(page: Page):
    to_do = blocks.ToDo("Task 0")
    page.append_children(to_do)

    assert is_valid_notion_id(to_do.id)
    assert to_do.text == "Task 0"

    to_do.text = "Task 1"
    assert to_do.text == "Task 1"

    assert to_do.checked == False
    to_do.checked = True
    assert to_do.checked == True

    to_do.uncheck()
    assert to_do.checked == False
    to_do.toggle_check()
    assert to_do.checked == True
    to_do.toggle_check()
    assert to_do.checked == False

    to_do.append_children(blocks.ToDo("Task 2"))
    assert to_do.checked == False
    assert to_do.children[0].checked == False
    to_do.check_all()
    assert to_do.checked == True
    assert to_do.children[0].checked == True

    to_do.delete()
    assert to_do.archived == True


def test_toggle_block(page: Page):
    toggle = blocks.Toggle("Toggle Text")
    page.append_children(toggle)

    assert is_valid_notion_id(toggle.id)
    assert toggle.text == "Toggle Text"

    toggle.append_children([blocks.Paragraph("Some unfoldable text")])
    assert [child.text for child in toggle.children] == ["Some unfoldable text"]

    toggle.delete()
    assert toggle.archived == True


def test_table_of_contents_block(page: Page):
    toc = blocks.TableOfContents()
    page.append_children(toc)

    assert is_valid_notion_id(toc.id)
    assert toc.color == "default"

    toc.color = "red"
    assert toc.color == "red"

    toc.delete()
    assert toc.archived == True


def test_breadcrumb_block(page: Page):
    breadcrumb = blocks.Breadcrumb()
    page.append_children(breadcrumb)

    assert is_valid_notion_id(breadcrumb.id)

    breadcrumb.delete()
    assert breadcrumb.archived == True


def test_equation_block(page: Page):
    equation = blocks.Equation("e=mc")
    page.append_children(equation)

    assert is_valid_notion_id(equation.id)

    equation.expression = "e=mc^2"
    assert equation.expression == "e=mc^2"

    equation.delete()
    assert equation.archived == True


def test_video_block(page: Page):
    video = blocks.Video("https://website.domain/files/video.mp4")
    page.append_children(video)

    assert is_valid_notion_id(video.id)
    assert video.url == "https://website.domain/files/video.mp4"

    video.url = "https://website.domain/files/video.mov"
    assert video.url == "https://website.domain/files/video.mov"

    video.delete()
    assert video.archived == True


def test_file_block(page: Page):
    file = blocks.File(url="https://website.domain/files/doc.txt")
    page.append_children(file)

    assert is_valid_notion_id(file.id)
    assert file.url == "https://website.domain/files/doc.txt"
    assert file.caption is None

    file.url = "https://website.domain/files/doc2.txt"
    file.caption = "The second doc"
    assert file.url == "https://website.domain/files/doc2.txt"
    assert file.caption == "The second doc"

    file.delete()
    assert file.archived == True


def test_pdf_block(page: Page):
    pdf = blocks.PDF("https://website.domain/files/doc.pdf")
    page.append_children(pdf)

    assert is_valid_notion_id(pdf.id)
    assert pdf.url == "https://website.domain/files/doc.pdf"

    pdf.url = "https://website.domain/files/doc2.pdf"
    assert pdf.url == "https://website.domain/files/doc2.pdf"

    pdf.delete()
    assert pdf.archived == True


def test_embed_block(page: Page):
    embed = blocks.Embed("https://twitter.com/Jack/status/20")
    page.append_children(embed)

    assert is_valid_notion_id(embed.id)
    assert embed.url == "https://twitter.com/Jack/status/20"

    embed.url = "https://twitter.com/james_kpatrick/status/320150923336892416"
    assert embed.url == "https://twitter.com/james_kpatrick/status/320150923336892416"

    embed.delete()
    assert embed.archived == True


def test_template_block(page: Page):
    template = blocks.Template("Some test template")
    page.append_children(template)

    assert is_valid_notion_id(template.id)
    assert template.text == "Some test template"
    assert template.children == []

    template.append_children(
        [blocks.HeadingOne("Test heading"), blocks.Paragraph("Test text")]
    )
    assert [child.text for child in template.children] == ["Test heading", "Test text"]

    template.delete()
    assert template.archived == True


def test_link_to_page_block(page: Page):
    # First create a test page we can link to.
    linkable_page = Page("Linkable Page")
    page.append_children(linkable_page)
    linkable_page = [
        child
        for child in page.children
        if isinstance(child, blocks.ChildPage) and child.title == "Linkable Page"
    ][0]

    link_to_page = blocks.LinkToPage(page_id=linkable_page.id)
    page.append_children(link_to_page)

    assert is_valid_notion_id(link_to_page.id)
    assert link_to_page.page_id == linkable_page.id
    assert link_to_page.database_id is None

    linkable_page.delete()
    assert linkable_page.archived == True
    link_to_page.delete()
    assert link_to_page.archived == True


def test_synced_block_block(page: Page):
    original_synced_block = blocks.SyncedBlock()
    page.append_children(original_synced_block)
    original_synced_block = [
        child for child in page.children if isinstance(child, blocks.SyncedBlock)
    ][0]
    original_synced_block.append_children(
        [blocks.Paragraph("Paragraph 1"), blocks.Paragraph("Paragraph 2")]
    )

    assert is_valid_notion_id(original_synced_block.id)
    assert len(original_synced_block.children) == 2

    reference_synced_block = blocks.SyncedBlock(original_synced_block.id)
    page.append_children(reference_synced_block)

    assert is_valid_notion_id(reference_synced_block.id)
    assert [child.text for child in reference_synced_block.children] == [
        "Paragraph 1",
        "Paragraph 2",
    ]

    original_synced_block.delete()
    assert original_synced_block.archived == True
    reference_synced_block.delete()
    assert reference_synced_block.archived == True


def test_column_blocks(page: Page):
    column_list = blocks.ColumnList(
        [blocks.Column([blocks.Paragraph(f"Column {i}")]) for i in (1, 2)]
    )
    page.append_children(column_list)

    assert is_valid_notion_id(column_list.id)
    columns = column_list.children
    assert len(columns) == 2
    assert all(isinstance(col, blocks.Column) for col in columns)
    assert all(is_valid_notion_id(col.id) for col in columns)
    assert all(col.children[0].text == f"Column {i+1}" for i, col in enumerate(columns))

    column_list.delete()
    assert column_list.archived == True


def test_table_blocks(page: Page):
    table = blocks.Table(
        table_width=2,
        children=[
            blocks.TableRow(cells=["Cell 1", "Cell 2"]),
            blocks.TableRow(cells=["Cell 3", "Cell 4"]),
        ],
    )
    page.append_children(table)

    assert is_valid_notion_id(table.id)
    assert len(table.children) == 2
    assert all(is_valid_notion_id(row.id) for row in table.rows)
    assert table.rows[0].cells == ["Cell 1", "Cell 2"]
    assert table.rows[1].cells == ["Cell 3", "Cell 4"]
    assert table.cells == [["Cell 1", "Cell 2"], ["Cell 3", "Cell 4"]]

    table.delete()
    assert table.archived == True


def test_getting_parent(page):
    """Test the parent property of pages.

    Assert the two possible cases that
    1. A page sits at the top-level as part of an workspace.
    2. A page is a child of another page.
    to_do: Add database parent as soon as database support is added.
    """
    page_parent = page.parent
    child_parent = page.children[4].parent

    assert isinstance(page_parent, ParentWorkspace)
    assert page_parent.to_json() == {"type": "workspace", "workspace": True}
    assert isinstance(child_parent, ParentPage)
    assert child_parent.to_json() == {"page_id": TEST_NOTION_PAGE, "type": "page_id"}


def test_deleting_all_children(page):
    "Delete all children to provide a clean slate for future tests."
    all_children = page.children
    for child in all_children:
        child.delete()

    assert all(child.archived for child in all_children)
    assert len(page.children) == 0
