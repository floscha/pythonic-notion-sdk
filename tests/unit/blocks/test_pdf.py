from notion.model.blocks import PDF


def test_pdf_internal_data():
    pdf = PDF("www.some.url/file.pdf")

    assert pdf._data == {
        "object": "block",
        "type": "pdf",
        "pdf": {"external": {"url": "www.some.url/file.pdf"}},
    }
