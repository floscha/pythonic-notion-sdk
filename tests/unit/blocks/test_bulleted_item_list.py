from notion.model.blocks.bulleted_list_item import BulletedListItem


def test_bookmark_internal_data():
    bulleted_list_item = BulletedListItem("Test Item")

    assert bulleted_list_item._data == {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {
            "rich_text": [{"type": "text", "text": {"content": "Test Item"}}],
            "color": "default",
        },
    }
