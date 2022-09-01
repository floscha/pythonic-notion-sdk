from notion.model.blocks import NumberedListItem


def test_numbered_list_item_internal_data():
    numbered_list_item = NumberedListItem("Some Item")

    assert numbered_list_item._data == {
        "object": "block",
        "type": "numbered_list_item",
        "numbered_list_item": {
            "rich_text": [{"type": "text", "text": {"content": "Some Item"}}],
            "color": "default",
        },
    }
