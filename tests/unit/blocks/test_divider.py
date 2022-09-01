from notion.model.blocks.divider import Divider


def test_breadcrumb_internal_data():
    divider = Divider()

    assert divider._data == {
        "object": "block",
        "type": "divider",
        "divider": {},
    }
