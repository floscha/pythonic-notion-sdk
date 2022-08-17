# Based on the example from https://developers.notion.com/reference/create-a-database
from os import environ

from pydotenvs import load_env

from notion import NotionClient
from notion.model.databases import Database
from notion.model.databases import properties as props

load_env()
TEST_NOTION_TOKEN = environ["TEST_NOTION_TOKEN"]
TEST_NOTION_PAGE = environ["TEST_NOTION_PAGE"]


client = NotionClient(TEST_NOTION_TOKEN)

meal_db = Database(
    title="Meals",
    properties={
        "Name": props.Title,
    },
).create(client, parent=TEST_NOTION_PAGE)

grocery_db = Database(
    title="Grocery List",
    icon="📝",
    properties={
        "Name": props.Title,
        "Description": props.RichText,
        "In stock": props.Checkbox,
        "Food group": props.Select(
            [
                props.SelectOption("🥦Vegetable", "green"),
                props.SelectOption("🍎Fruit", "red"),
                props.SelectOption("💪Protein", "yellow"),
            ]
        ),
        "Price": props.Number(format="dollar"),
        "Last ordered": props.Date,
        "Meals": props.Relation(meal_db.id, "single_property"),
        "Number of meals": props.Rollup("Name", "Meals", "count"),
        "Store availability": props.MultiSelect(
            [
                props.SelectOption("Duc Loi Market", "blue"),
                props.SelectOption("Rainbow Grocery", "gray"),
                props.SelectOption("Nijiya Market", "purple"),
                props.SelectOption("Gus's Community Market", "yellow"),
            ]
        ),
        "+1": props.People,
        "Photo": props.Files,
    },
).create(client, parent=TEST_NOTION_PAGE)
