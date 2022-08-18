from os import environ

from pydotenvs import load_env
from pytest import fixture

from notion import NotionClient
from notion.model.common import is_valid_notion_id
from notion.model.page import Page
from notion.model.users import Bot, Person, User

load_env()
TEST_NOTION_TOKEN = environ["TEST_NOTION_TOKEN"]
TEST_NOTION_PAGE = environ["TEST_NOTION_PAGE"]


@fixture
def client() -> NotionClient:
    return NotionClient(TEST_NOTION_TOKEN)


@fixture
def page(client: NotionClient) -> Page:
    return client.get_page(TEST_NOTION_PAGE)


def test_getting_all_users(client: NotionClient):
    users = client.users.get_all()

    assert all(isinstance(user_object, User) for user_object in users)
    assert all(is_valid_notion_id(user_object.id) for user_object in users)


def test_getting_token_owner(client: NotionClient):
    token_owner = client.users.get_token_owner()

    assert isinstance(token_owner, Bot)
    assert is_valid_notion_id(token_owner.id)
    assert token_owner.name == "pythonic-notion-sdk"


def test_finding_my_user(client: NotionClient):
    all_users = client.users.get_all()
    results = [user for user in all_users if isinstance(user, Person)]

    assert len(results) == 1
    assert results[0].name == "Florian Schäfer"
