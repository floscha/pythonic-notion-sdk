from os import environ

import requests
from pydotenvs import load_env

load_env()
TEST_NOTION_TOKEN = environ["TEST_NOTION_TOKEN"]
TEST_NOTION_PAGE = environ["TEST_NOTION_PAGE"]


headers = {
    "Accept": "application/json",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
    "Authorization": TEST_NOTION_TOKEN,
}

# Create database
todo_db_data = {
    "parent": {"type": "page_id", "page_id": TEST_NOTION_PAGE},
    "icon": {
        "type": "external",
        "external": {"url": "https://super.so/icon/dark/check-square.svg"},
    },
    "title": [
        {
            "type": "text",
            "text": {
                "content": "ToDo List",
            },
        }
    ],
    "properties": {
        "Name": {"title": {}},
        "Done": {"checkbox": {}},
    },
}
todo_database_id = requests.post(
    "https://api.notion.com/v1/databases", headers=headers, json=todo_db_data
).json()["id"]


# Add pages to database
for page_title, is_done in zip(("Item 1", "Item 2", "Item 3"), (False, True, False)):
    todo_page_data = {
        "parent": {"database_id": todo_database_id},
        "properties": {
            "Name": {"title": [{"text": {"content": page_title}}]},
            "Done": {"checkbox": is_done},
        },
    }
    requests.post(
        "https://api.notion.com/v1/pages", headers=headers, json=todo_page_data
    )

# Query database for certain property
filter_data = {"property": "Done", "checkbox": {"equals": False}}
open_tasks = requests.post(
    f"https://api.notion.com/v1/databases/{todo_database_id}/query",
    headers=headers,
    json={"filter": filter_data},
).json()["results"]
for task in open_tasks:
    page_id = task["id"]
    title_property_id = task["properties"]["Name"]["id"]
    title = requests.get(
        f"https://api.notion.com/v1/pages/{page_id}/properties/{title_property_id}",
        headers=headers,
    ).json()["results"][0]
    print(title["title"]["text"]["content"])

# Delete database
requests.patch(
    f"https://api.notion.com/v1/databases/{todo_database_id}",
    headers=headers,
    json={"archived": True},
)
