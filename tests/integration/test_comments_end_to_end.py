from os import environ

from pydotenvs import load_env
from pytest import fixture

from notion import NotionClient
from notion.model.comment import Comment
from notion.model.page import Page

load_env()
TEST_NOTION_TOKEN = environ["TEST_NOTION_TOKEN"]
TEST_NOTION_PAGE = environ["TEST_NOTION_PAGE"]


@fixture
def client() -> NotionClient:
    return NotionClient(TEST_NOTION_TOKEN)


@fixture
def page(client: NotionClient) -> Page:
    return client.pages.get(TEST_NOTION_PAGE)


def test_comments(page: Page):
    page.append_children(Page("Comment Test Page"))
    comment_test_page = page.children[0]

    test_comment = Comment(comment_test_page.id, "Test Comment")
    page._client.comments.create(test_comment)

    comments = page._client.comments.get(comment_test_page.id)
    assert len(comments) == 1
    assert comments[0].text == "Test Comment"

    comment_test_page.delete()
