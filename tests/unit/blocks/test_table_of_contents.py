from notion.model.blocks import TableOfContents


def test_table_of_contents_internal_data():
    table_of_contents = TableOfContents()

    assert table_of_contents._data == {
        "object": "block",
        "type": "table_of_contents",
        "table_of_contents": {"color": "default"},
    }
