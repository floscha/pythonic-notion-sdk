from notion.model.blocks import Table


def test_table_internal_data():
    table = Table()

    assert table._data == {
        "object": "block",
        "type": "table",
        "table": {
            "table_width": None,
            "has_column_header": False,
            "has_row_header": False,
        },
    }
