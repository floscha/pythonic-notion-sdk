import re
from datetime import datetime, timezone
from os import environ

from pydotenvs import load_env
from pytest import fixture

from notion import NotionClient
from notion.model.block import *
from notion.model.colors import Colors
from notion.model.page import *


load_env()
TEST_NOTION_TOKEN = environ["TEST_NOTION_TOKEN"]
TEST_NOTION_PAGE = environ["TEST_NOTION_PAGE"]


@fixture
def client():
    return NotionClient(TEST_NOTION_TOKEN)


@fixture
def page(client):
    return client.get_page(TEST_NOTION_PAGE)


def is_valid_notion_id(id_str: str) -> bool:
    id_regex = r"^[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12}$"
    match = re.search(id_regex, id_str)
    return bool(match)


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


def test_page_has_no_children(page):
    "At the beginning of the integration tests, the page should have no children."
    assert page.children == []


def test_adding_children(page):
    """Test adding various blocks and pages as children.

    Especially validate that adding a list of BOTH blocks and pages works, as the official API
    supports adding a list of block only.
    """
    page.append_children(
        [
            HeadingOne("Heading 1"),
            HeadingTwo("Heading 2"),
            HeadingThree("Heading 3"),
            Paragraph("Some Text"),
            Page("Sub Page"),
            Quote("Some Quote"),
        ]
    )

    all_children = page.children
    assert all_children[0].object == "block"
    assert all_children[0].type == "heading_1"
    assert all_children[1].object == "block"
    assert all_children[1].type == "heading_2"
    assert all_children[2].object == "block"
    assert all_children[2].type == "heading_3"
    assert all_children[3].object == "block"
    assert all_children[3].type == "paragraph"
    assert all_children[4].object == "block"
    assert all_children[4].type == "child_page"
    assert all_children[5].object == "block"
    assert all_children[5].type == "quote"


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


def test_callout_block(page):
    callout = Callout("Some Text", "⭐", Colors.green, children=[Quote("Some Quote")])
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
    code = Code("print('Hello World')")
    page.append_children(code)

    assert is_valid_notion_id(code.id)
    assert code.text == "print('Hello World')"
    assert code.language == "plain text"

    code.language = "python"
    assert code.language == "python"

    code.delete()
    assert code.archived == True


def test_divider_block(page: Page):
    divider = Divider()
    page.append_children(divider)

    assert is_valid_notion_id(divider.id)

    divider.delete()
    assert divider.archived == True


def test_bookmark_block(page: Page):
    bookmark = Bookmark(url="https://www.notion.so")
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
    image = Image("https://super.so/icon/dark/image.svg")
    page.append_children(image)

    assert is_valid_notion_id(image.id)
    assert image.url == "https://super.so/icon/dark/image.svg"

    image.url = "https://super.so/icon/dark/home.svg"
    assert image.url == "https://super.so/icon/dark/home.svg"

    image.delete()
    assert image.archived == True


def test_bulleted_list_item_block(page: Page):
    bulleted_list = BulletedListItem("Item B")
    page.append_children(bulleted_list)

    assert is_valid_notion_id(bulleted_list.id)
    assert bulleted_list.text == "Item B"

    bulleted_list.text = "Item A"
    assert bulleted_list.text == "Item A"

    bulleted_list.append_children(
        [BulletedListItem("Item a"), BulletedListItem("Item b")]
    )
    assert [child.text for child in bulleted_list.children] == ["Item a", "Item b"]

    bulleted_list.delete()
    assert bulleted_list.archived == True


def test_numbered_list_item_block(page: Page):
    numbered_list = NumberedListItem("Item B")
    page.append_children(numbered_list)

    assert is_valid_notion_id(numbered_list.id)
    assert numbered_list.text == "Item B"

    numbered_list.text = "Item A"
    assert numbered_list.text == "Item A"

    numbered_list.append_children(
        [NumberedListItem("Item a"), NumberedListItem("Item b")]
    )
    assert [child.text for child in numbered_list.children] == ["Item a", "Item b"]

    numbered_list.delete()
    assert numbered_list.archived == True


def test_to_do_block(page: Page):
    to_do = ToDo("Task 0")
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

    to_do.append_children(ToDo("Task 2"))
    assert to_do.checked == False
    assert to_do.children[0].checked == False
    to_do.check_all()
    assert to_do.checked == True
    assert to_do.children[0].checked == True

    to_do.delete()
    assert to_do.archived == True


def test_toggle_block(page: Page):
    toggle = Toggle("Toggle Text")
    page.append_children(toggle)

    assert is_valid_notion_id(toggle.id)
    assert toggle.text == "Toggle Text"

    toggle.append_children([Paragraph("Some unfoldable text")])
    assert [child.text for child in toggle.children] == ["Some unfoldable text"]

    toggle.delete()
    assert toggle.archived == True


def test_table_of_contents_block(page: Page):
    toc = TableOfContents()
    page.append_children(toc)

    assert is_valid_notion_id(toc.id)
    assert toc.color == "default"

    toc.color = "red"
    assert toc.color == "red"

    toc.delete()
    assert toc.archived == True


def test_breadcrumb_block(page: Page):
    breadcrumb = Breadcrumb()
    page.append_children(breadcrumb)

    assert is_valid_notion_id(breadcrumb.id)

    breadcrumb.delete()
    assert breadcrumb.archived == True


def test_equation_block(page: Page):
    equation = Equation("e=mc")
    page.append_children(equation)

    assert is_valid_notion_id(equation.id)

    equation.expression = "e=mc^2"
    assert equation.expression == "e=mc^2"

    equation.delete()
    assert equation.archived == True


def test_getting_parent(page):
    """Test the parent property of pages.

    Assert the two possible cases that
    1. A page sits at the top-level as part of an workspace.
    2. A page is a child of another page.
    to_do: Add database parent as soon as database support is added.
    """
    assert page.parent == {"type": "workspace", "workspace": True}
    assert page.children[4].parent == {"page_id": TEST_NOTION_PAGE, "type": "page_id"}


def test_deleting_all_children(page):
    "Delete all children to provide a clean slate for future tests."
    all_children = page.children
    for child in all_children:
        child.delete()

    # assert len([child for child in all_children if child.archived == True ]) == len(all_children)
    assert all(child.archived for child in all_children)
    assert len(page.children) == 0
