from notion.model.blocks import Embed


def test_embed_internal_data():
    code = Embed("www.notion.so")

    assert code._data == {
        "object": "block",
        "type": "embed",
        "embed": {"url": "www.notion.so"},
    }
