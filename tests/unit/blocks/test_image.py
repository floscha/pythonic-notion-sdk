from notion.model.blocks import Image


def test_image_internal_data():
    image = Image("www.notion.so")

    assert image._data == {
        "object": "block",
        "type": "image",
        "image": {"external": {"url": "www.notion.so"}},
    }
