from notion.model import filters

# ---------------------------------------------------------------------------
# Example from https://developers.notion.com/reference/post-database-query
# ---------------------------------------------------------------------------


def test_reference_example():
    expected_json_output = {
        "and": [
            {"property": "Done", "checkbox": {"equals": True}},
            {
                "or": [
                    {"property": "Tags", "contains": "A"},
                    {"property": "Tags", "contains": "B"},
                ]
            },
        ]
    }
    test_filter = filters.And(
        [
            filters.Checkbox("Done").equals(True),
            filters.Or(
                [
                    filters.MultiSelect("Tags").contains("A"),
                    filters.MultiSelect("Tags").contains("B"),
                ]
            ),
        ]
    )

    assert test_filter.to_json() == expected_json_output


def test_reference_example_with_logical_operators():
    expected_json_output = {
        "and": [
            {"property": "Done", "checkbox": {"equals": True}},
            {
                "or": [
                    {"property": "Tags", "contains": "A"},
                    {"property": "Tags", "contains": "B"},
                ]
            },
        ]
    }

    test_filter = filters.Checkbox("Done").equals(True) & (
        filters.MultiSelect("Tags").contains("A")
        | filters.MultiSelect("Tags").contains("B")
    )

    assert test_filter.to_json() == expected_json_output


# ---------------------------------------------------------------------------
# Tests for all `Filter` classes
# ---------------------------------------------------------------------------


def test_timestamp_filter():
    expected_json_output = {
        "timestamp": "created_time",
        "created_time": {"past_week": {}},
    }

    timestamp_filter = filters.Timestamp("created_time").past_week()

    assert timestamp_filter.to_json() == expected_json_output


def test_formula_checkbox_filter():
    expected_json_output = {"property": "Formula", "checkbox": {"equals": True}}

    formula_checkbox_filter = filters.Formula(filters.Checkbox("Formula").equals(True))

    assert formula_checkbox_filter.to_json() == expected_json_output


def rollup_number_filter():
    expected_json_output = {"property": "Todo Count", "number": {"equals": 2}}

    rollup_number_filter = filters.Rollup(filters.Number("Todo Count").equals(2))

    assert rollup_number_filter.to_json() == expected_json_output


# TODO: Add the remaining filters.
