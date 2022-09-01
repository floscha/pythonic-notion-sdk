from notion.model.blocks.heading import HeadingOne, HeadingThree, HeadingTwo


def test_heading_1_internal_data():
    heading_1 = HeadingOne("Test Heading")

    assert heading_1._data == {
        "object": "block",
        "type": "heading_1",
        "heading_1": {
            "rich_text": [{"type": "text", "text": {"content": "Test Heading"}}]
        },
    }


def test_heading_2_internal_data():
    heading_2 = HeadingTwo("Test Heading")

    assert heading_2._data == {
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [{"type": "text", "text": {"content": "Test Heading"}}]
        },
    }


def test_heading_3_internal_data():
    heading_3 = HeadingThree("Test Heading")

    assert heading_3._data == {
        "object": "block",
        "type": "heading_3",
        "heading_3": {
            "rich_text": [{"type": "text", "text": {"content": "Test Heading"}}]
        },
    }
