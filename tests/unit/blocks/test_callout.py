from notion.model.blocks import Callout
from notion.model.properties.emoji import Emoji


def test_callout_internal_data():
    callout = Callout("Some Text", Emoji("⭐"))

    assert callout._data == {
        "object": "block",
        "type": "callout",
        "callout": {
            "rich_text": [{"type": "text", "text": {"content": "Some Text"}}],
            "color": "default",
            "icon": {"emoji": "⭐", "type": "emoji"},
        },
    }
