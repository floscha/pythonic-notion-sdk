from notion.model.blocks.breadcrumb import Breadcrumb


def test_breadcrumb_internal_data():
    breadcrumb = Breadcrumb()

    assert breadcrumb._data == {
        "object": "block",
        "type": "breadcrumb",
        "breadcrumb": {},
    }
