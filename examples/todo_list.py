from os import environ

from pydotenvs import load_env

import notion.model.databases.properties as prop
from notion import NotionClient
from notion.model import filters
from notion.model.databases.database import Database
from notion.model.page import Page


load_env()
TEST_NOTION_TOKEN = environ["TEST_NOTION_TOKEN"]
TEST_NOTION_PAGE = environ["TEST_NOTION_PAGE"]


client = NotionClient(TEST_NOTION_TOKEN)

# Create database
todo_db = Database(
    title="ToDo List",
    icon="https://super.so/icon/dark/check-square.svg",
    properties={"Done": prop.Checkbox},
).create(client, TEST_NOTION_PAGE)

# Add pages to database
todo_db += Page("Item 1")
todo_db += Page("Item 2", properties={"Done": prop.Checkbox(True)})
todo_db += Page("Item 3")

# Query database for certain property
open_tasks = todo_db.query(filters.Checkbox("Done").equals(False))
print([task.title for task in open_tasks])

# Delete database
todo_db.delete()
