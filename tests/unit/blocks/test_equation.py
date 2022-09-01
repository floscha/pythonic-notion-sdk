from notion.model.blocks import Equation


def test_equation_internal_data():
    equation = Equation("Test Expression")

    assert equation._data == {
        "object": "block",
        "type": "equation",
        "equation": {"expression": "Test Expression"},
    }
