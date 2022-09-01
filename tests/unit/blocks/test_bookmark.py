from notion.model.blocks.bookmark import Bookmark


def test_bookmark_internal_data():
    bookmark = Bookmark("www.notion.so", "Test Caption")

    assert bookmark._data == {
        "object": "block",
        "type": "bookmark",
        "bookmark": {
            "url": "www.notion.so",
            "caption": [{"text": {"content": "Test Caption"}}],
        },
    }
