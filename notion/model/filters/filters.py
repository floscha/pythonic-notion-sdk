from abc import ABC, abstractmethod
from typing import List, Optional, Union

from notion.model.common.utils import UUIDv4, class_name_as_snake_case
from notion.model.filters.conditions import *

# ---------------------------------------------------------------------------
# Filter Base Class
# ---------------------------------------------------------------------------


class Filter(ABC):
    def __init__(self, target: str, condition: Optional[Union["Filter", List]] = None):
        self.target = target
        self.condition = condition

    def __and__(self, other: "Filter") -> "Filter":
        return And([self, other])

    def __or__(self, other: "Filter") -> "Filter":
        return Or([self, other])

    def with_condition(self, condition: Condition) -> "Filter":
        self.condition = condition
        return self

    @abstractmethod
    def to_json(self) -> dict:
        pass


# ---------------------------------------------------------------------------
# Compound Filter
# ---------------------------------------------------------------------------


class Compound(Filter):
    """A compound filter object combines several filter objects together using a logical operator and or or.
    A compound filter can even be combined within a compound filter, but only up to two nesting levels deep.

    Docs: https://developers.notion.com/reference/post-database-query-filter#compound-filter-object
    """

    def to_json(self) -> dict:
        return {self.target: [con.to_json() for con in self.condition]}


def And(filters: List[Filter]):
    return Compound("and", filters)


def Or(filters: List[Filter]):
    return Compound("or", filters)


# ---------------------------------------------------------------------------
# Type-specific Filters
# ---------------------------------------------------------------------------


class PropertyFilter(Filter):
    "Abstract class for all `Filter` subclasses that filter based on some database property."

    def to_json(self):
        return {"property": self.target, **self.condition.to_json()}


class Text(PropertyFilter):
    """A text filter condition can be applied to database properties of types `Title`, `RichText`, `URL`, `Email`, and `PhoneNumber`.

    Docs: https://developers.notion.com/reference/post-database-query-filter#text-filter-condition
    """

    def equals(self, string: str):
        "Only return pages where the page property value matches the provided value exactly."
        return self.with_condition(Equals(string))

    def does_not_equal(self, string: str):
        "Only return pages where the page property value does not match the provided value exactly."
        return self.with_condition(DoesNotEqual(string))

    def contains(self, string: str):
        "Only return pages where the page property value contains the provided value."
        return self.with_condition(Contains(string))

    def does_not_contain(self, string: str):
        "Only return pages where the page property value does not contain the provided value."
        return self.with_condition(DoesNotContain(string))

    def starts_with(self, string: str):
        "Only return pages where the page property value starts with the provided value."
        return self.with_condition(StartsWith(string))

    def ends_with(self, string: str):
        "Only return pages where the page property value ends with the provided value."
        return self.with_condition(EndsWith(string))

    def is_empty(self):
        "Only return pages where the page property value is empty."
        return self.with_condition(IsEmpty())

    def is_not_empty(self):
        "Only return pages where the page property value is present."
        return self.with_condition(IsNotEmpty())


class Number(PropertyFilter):
    """A number filter condition can be applied to database properties of type `Number`.

    Docs: https://developers.notion.com/reference/post-database-query-filter#number-filter-condition
    """

    def equals(self, number: int):
        "Only return pages where the page property value matches the provided value exactly."
        return self.with_condition(Equals(number))

    def does_not_equal(self, number: int):
        "Only return pages where the page property value does not match the provided value exactly."
        return self.with_condition(DoesNotEqual(number))

    def greater_than(self, number: int):
        "Only return pages where the page property value is greater than the provided value."
        return self.with_condition(GreaterThan(number))

    def less_than(self, number: int):
        "Only return pages where the page property value is less than the provided value."
        return self.with_condition(LessThan(number))

    def greater_than_or_equal_to(self, number: int):
        "Only return pages where the page property value is greater than or equal to the provided value."
        return self.with_condition(GreaterThanOrEqualTo(number))

    def less_than_or_equal_to(self, number: int):
        "Only return pages where the page property value is less than or equal to the provided value."
        return self.with_condition(LessThanOrEqualTo(number))

    def is_empty(self):
        "Only return pages where the page property value is empty."
        return self.with_condition(IsEmpty())

    def is_not_empty(self):
        "Only return pages where the page property value is present."
        return self.with_condition(IsNotEmpty())

    def to_json(self) -> dict:
        return {"property": self.target, "number": self.condition.to_json()}


class Checkbox(PropertyFilter):
    """A checkbox filter condition can be applied to database properties of type `checkbox`.

    Docs: https://developers.notion.com/reference/post-database-query-filter#checkbox-filter-condition
    """

    def equals(self, checked: bool):
        return self.with_condition(Equals(checked))

    def does_not_equal(self, checked: bool):
        return self.with_condition(DoesNotEqual(checked))

    def to_json(self):
        return {"property": self.target, "checkbox": self.condition.to_json()}


class Select(PropertyFilter):
    """A select filter condition can be applied to database properties of type `Select`.

    Docs: https://developers.notion.com/reference/post-database-query-filter#select-filter-condition
    """

    def equals(self, string: str):
        "Only return pages where the page property value matches the provided value exactly."
        return self.with_condition(Equals(string))

    def does_not_equal(self, string: str):
        "Only return pages where the page property value does not match the provided value exactly."
        return self.with_condition(DoesNotEqual(string))

    def is_empty(self):
        "Only return pages where the page property value is empty."
        return self.with_condition(IsEmpty())

    def is_not_empty(self) -> dict:
        "Only return pages where the page property value is present."
        return self.with_condition(IsNotEmpty())


class MultiSelect(PropertyFilter):
    """A multi-select filter condition can be applied to database properties of type `MultiSelect`.

    Docs: https://developers.notion.com/reference/post-database-query-filter#multi-select-filter-condition
    """

    def contains(self, string: str) -> "MultiSelect":
        "Only return pages where the page property value contains the provided value."
        return self.with_condition(Contains(string))

    def does_not_contain(self, string: str) -> "MultiSelect":
        "Only return pages where the page property value does not contain the provided value."
        return self.with_condition(DoesNotContain(string))

    def is_empty(self) -> "MultiSelect":
        "Only return pages where the page property value is empty."
        return self.with_condition(IsEmpty())

    def is_not_empty(self) -> "MultiSelect":
        "Only return pages where the page property value is present."
        return self.with_condition(IsNotEmpty())


class Date(PropertyFilter):
    """A date filter condition can be applied to database properties of types `Date`, `created_time`, and `last_edited_time`.

    Docs: https://developers.notion.com/reference/post-database-query-filter#date-filter-condition
    """

    def equals(self, date: str):  # (ISO 8601 date)
        """Only return pages where the page property value matches the provided date exactly.
        If a date is provided, the comparison is done against the start and end of the UTC date.
        If a date with a time is provided, the comparison is done with millisecond precision.
        Note that if no timezone is provided, the default is UTC.	"2021-05-10" or "2021-05-10T12:00:00" or "2021-10-15T12:00:00-07:00"
        """
        return self.with_condition(Equals(date))

    def before(self, date: str):  # (ISO 8601 date)
        """Only return pages where the page property value is before the provided date.
        If a date with a time is provided, the comparison is done with millisecond precision.
        Note that if no timezone is provided, the default is UTC.	"2021-05-10" or "2021-05-10T12:00:00" or "2021-10-15T12:00:00-07:00"
        """
        return self.with_condition(Before(date))

    def after(self, date: str):  # (ISO 8601 date)
        """Only return pages where the page property value is after the provided date.
        If a date with a time is provided, the comparison is done with millisecond precision.
        Note that if no timezone is provided, the default is UTC.	"2021-05-10" or "2021-05-10T12:00:00" or "2021-10-15T12:00:00-07:00"
        """
        return self.with_condition(After(date))

    def on_or_before(self, date: str):  # (ISO 8601 date)
        """Only return pages where the page property value is on or before the provided date.
        If a date with a time is provided, the comparison is done with millisecond precision.
        Note that if no timezone is provided, the default is UTC.	"2021-05-10" or "2021-05-10T12:00:00" or "2021-10-15T12:00:00-07:00"
        """
        return self.with_condition(OnOrBefore(date))

    def on_or_after(self, date: str):  # (ISO 8601 date)
        """Only return pages where the page property value is on or after the provided date.
        If a date with a time is provided, the comparison is done with millisecond precision.
        Note that if no timezone is provided, the default is UTC.	"2021-05-10" or "2021-05-10T12:00:00" or "2021-10-15T12:00:00-07:00"
        """
        return self.with_condition(OnOrAfter(date))

    def is_empty(self):
        "Only return pages where the page property value is empty."
        return self.with_condition(IsEmpty())

    def is_not_empty(self):
        "Only return pages where the page property value is present."
        return self.with_condition(IsNotEmpty())

    def past_week(self):
        "Only return pages where the page property value is within the past week."
        return self.with_condition(PastWeek())

    def past_month(self):
        "Only return pages where the page property value is within the past month."
        return self.with_condition(PastMonth())

    def past_year(self):
        "Only return pages where the page property value is within the past year."
        return self.with_condition(PastYear())

    def next_week(self):
        "Only return pages where the page property value is within the next week."
        return self.with_condition(NextWeek())

    def next_month(self):
        "Only return pages where the page property value is within the next month."
        return self.with_condition(NextMonth())

    def next_year(self):
        "Only return pages where the page property value is within the next year."
        return self.with_condition(NextYear())


class Timestamp(Date):
    """A specialized `Date` filter for the timestamps "created_time" and "last_edited_time".

    Docs: https://developers.notion.com/reference/post-database-query-filter#timestamp-filter-object
    """

    def __post_init__(self):
        if self.property not in ("created_time", "last_edited_time"):
            raise ValueError(f"Timestamp property {self.property!r} is not supported.")

    def to_json(self):
        return {"timestamp": self.target, self.target: self.condition.to_json()}


class People(PropertyFilter):
    """A people filter condition can be applied to database properties of types `People`, `created_by`, and `last_edited_by`.

    Docs: https://developers.notion.com/reference/post-database-query-filter#people-filter-condition
    """

    def contains(self, string: UUIDv4):
        """Only return pages where the page property value contains the provided value."""
        return self.with_condition(Contains(string))

    def does_not_contain(self, string: UUIDv4):
        """Only return pages where the page property value does not contain the provided value."""
        return self.with_condition(DoesNotContain(string))

    def is_empty(self):
        "Only return pages where the page property value is empty."
        return self.with_condition(IsEmpty())

    def is_not_empty(self):
        "Only return pages where the page property value is present."
        return self.with_condition(IsNotEmpty())


class Files(PropertyFilter):
    """A files filter condition can be applied to database properties of type `Files`.

    Docs: https://developers.notion.com/reference/post-database-query-filter#files-filter-condition
    """

    def is_empty(self):
        "Only return pages where the page property value is empty."
        return self.with_condition(IsEmpty())

    def is_not_empty(self):
        "Only return pages where the page property value is present."
        return self.with_condition(IsNotEmpty())


class Relation(PropertyFilter):
    """A relation filter condition can be applied to database properties of type `Relation`.

    Docs: https://developers.notion.com/reference/post-database-query-filter#relation-filter-condition
    """

    def contains(self, string: UUIDv4):
        """Only return pages where the page property value contains the provided value."""
        return self.with_condition(Contains(string))

    def does_not_contain(self, string: UUIDv4):
        """Only return pages where the page property value does not contain the provided value."""
        return self.with_condition(DoesNotContain(string))

    def is_empty(self):
        "Only return pages where the page property value is empty."
        return self.with_condition(IsEmpty())

    def is_not_empty(self):
        "Only return pages where the page property value is present."
        return self.with_condition(IsNotEmpty())


class Rollup(Filter):
    """A rollup filter condition can be applied to database properties of type "rollup".

    Rollups which evaluate to arrays accept a filter with an any, every, or none condition;
        rollups which evaluate to numbers accept a filter with a number condition;
        and rollups which evaluate to dates accept a filter with a date condition.
    Rollups which evaluate to arrays accept any kind of property in

    Supports the following rollup types:
    - array: See `any`, `every`, and `none` methods.
    - number: For a rollup property which evaluates to an number, return the pages where the number fits this criterion.
    - date: For a rollup property which evaluates to an date, return the pages where the date fits this criterion.

    Docs: https://developers.notion.com/reference/post-database-query-filter#rollup-filter-condition
    """

    def __init__(
        self, filter_: Union[Number, Date], array_condition: Optional[str] = None
    ) -> Filter:
        super().__init__(filter_.target, filter_.condition)

        self.filter_name = class_name_as_snake_case(filter_)
        # Manually patch naming inconsistency.
        if self.filter_name == "text":
            self.filter_name = "rich_text"
        self.array_condition = array_condition

    @staticmethod
    def any(filter_: Filter) -> "Rollup":
        """For a rollup property which evaluates to an array, return the pages where any item in that rollup fits this criterion.
        The criterion itself can be any other property type."""
        return Rollup(filter_, "any")

    @staticmethod
    def every(filter_: Filter) -> "Rollup":
        """For a rollup property which evaluates to an array, return the pages where every item in that rollup fits this criterion.
        The criterion itself can be any other property type."""
        return Rollup(filter_, "every")

    @staticmethod
    def none(filter_: Filter) -> "Rollup":
        """For a rollup property which evaluates to an array, return the pages where no item in that rollup fits this criterion.
        The criterion itself can be any other property type."""
        return Rollup(filter_, "none")

    def to_json(self) -> dict:
        if self.array_condition:
            return {
                "property": self.target,
                "rollup": {
                    self.array_condition: {self.filter_name: self.condition.to_json()}
                },
            }
        else:
            return {
                "property": self.target,
                "rollup": {self.filter_name: self.condition.to_json()},
            }


class Formula(Filter):
    """A formula filter condition can be applied to database properties of type `Formula`.

    `filter_` can be a
    - `Text` filter condition: Only return pages where the result type of the page property formula is "string" and the provided string filter condition matches the formula's value.
    - `Checkbox` filter condition: Only return pages where the result type of the page property formula is "checkbox" and the provided checkbox filter condition matches the formula's value.
    - `Number` filter condition): Only return pages where the result type of the page property formula is "number" and the provided number filter condition matches the formula's value.
    - `Date` filter condition: Only return pages where the result type of the page property formula is "date" and the provided date filter condition matches the formula's value.

    Docs: https://developers.notion.com/reference/post-database-query-filter#formula-filter-condition
    """

    def __init__(self, filter_: Filter) -> Filter:
        super().__init__(filter_.target, filter_.condition)
        self.filter_name = class_name_as_snake_case(filter_)

    def to_json(self) -> dict:
        return {"property": self.target, self.filter_name: self.condition.to_json()}
