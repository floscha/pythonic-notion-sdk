from notion.model.blocks.paragraph import Paragraph


def test_paragraph_internal_data():
    paragraph = Paragraph("Some Text")

    assert paragraph._data == {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{"type": "text", "text": {"content": "Some Text"}}]
        },
    }
