import re
from datetime import datetime, timezone
from os import environ

from pydotenvs import load_env
from pytest import fixture

from notion import NotionClient
from notion.model.block import *
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
            Heading("Heading 1"),
            SubHeading("Heading 2"),
            SubSubHeading("Heading 3"),
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


def test_getting_parent(page):
    """Test the parent property of pages.

    Assert the two possible cases that
    1. A page sits at the top-level as part of an workspace.
    2. A page is a child of another page.
    TODO: Add database parent as soon as database support is added.
    """
    assert page.parent == {"type": "workspace", "workspace": True}
    assert page.children[4].parent == {"page_id": TEST_NOTION_PAGE, "type": "page_id"}


def test_deleting_all_children(page):
    "Delete all children to provide a clean slate for future tests."
    for child in page.children:
        child.delete()

    assert len(page.children) == 0
