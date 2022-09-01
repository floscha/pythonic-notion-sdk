from notion.model.blocks import Code


def test_code_internal_data():
    code = Code("Some Code")

    assert code._data == {
        "object": "block",
        "type": "code",
        "code": {
            "rich_text": [{"type": "text", "text": {"content": "Some Code"}}],
            "language": "plain text",
        },
    }
