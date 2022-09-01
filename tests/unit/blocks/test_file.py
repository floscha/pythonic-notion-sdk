from notion.model.blocks import File


def test_file_internal_data():
    file = File("www.notion.so", caption="Test Caption")

    assert file._data == {
        "object": "block",
        "type": "file",
        "file": {
            "external": {"url": "www.notion.so"},
            "caption": [{"text": {"content": "Test Caption"}}],
        },
    }
