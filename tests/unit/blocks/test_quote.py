from notion.model.blocks import Quote


def test_quote_internal_data():
    quote = Quote("Some Quote")

    assert quote._data == {
        "object": "block",
        "type": "quote",
        "quote": {"rich_text": [{"type": "text", "text": {"content": "Some Quote"}}]},
    }
