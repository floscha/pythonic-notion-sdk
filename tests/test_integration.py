from os import environ

from pydotenvs import load_env
from pytest import fixture

from notion import NotionClient
from notion.model import *


load_env()


@fixture
def client():
    return NotionClient(environ["TEST_NOTION_TOKEN"])


@fixture
def page(client):
    return client.get_page(environ["TEST_NOTION_PAGE"])


def test_creating_client(client):
    "Simply check if a Notion client can be created."
    assert isinstance(client, NotionClient)


def test_getting_test_page(page):
    "Check if the test page can be retrieved and has the correct title."
    assert page.title == "pythonic-notion-playground"


def test_page_has_no_block_children(page):
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
    assert all_children[0].text == "Heading 1"
    assert all_children[1].text == "Heading 2"
    assert all_children[2].text == "Heading 3"
    assert all_children[3].text == "Some Text"
    assert all_children[4].title == "Sub Page"
    assert all_children[5].text == "Some Quote"


def test_deleting_all_children(page):
    "Delete all children to provide a clean slate for future tests."
    for child in page.children:
        child.delete()

    assert len(page.children) == 0
