from notion.model.blocks.link_preview import LinkPreview


def test_bookmark_internal_data():
    link_preview = LinkPreview("www.notion.so")

    assert link_preview._data == {
        "object": "block",
        "type": "link_preview",
        "link_preview": {
            "url": "www.notion.so",
        },
    }
