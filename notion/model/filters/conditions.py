from abc import abstractmethod
from typing import Any

from notion.model.common.utils import class_name_as_snake_case


class Condition:
    @abstractmethod
    def to_json(self):
        pass


class TrueCondition(Condition):
    def to_json(self) -> dict:
        return {class_name_as_snake_case(self): True}


class ObjectCondition(Condition):
    def to_json(self) -> dict:
        return {class_name_as_snake_case(self): {}}


class ValuedCondition(Condition):
    def __init__(self, value: Any):
        self.value = value

    def to_json(self) -> dict:
        return {class_name_as_snake_case(self): self.value}


class Equals(ValuedCondition):
    pass


class DoesNotEqual(ValuedCondition):
    pass


class Contains(ValuedCondition):
    pass


class DoesNotContain(ValuedCondition):
    pass


class StartsWith(ValuedCondition):
    pass


class EndsWith(ValuedCondition):
    pass


class IsEmpty(TrueCondition):
    pass


class IsNotEmpty(TrueCondition):
    pass


class GreaterThan(ValuedCondition):
    pass


class LessThan(ValuedCondition):
    pass


class GreaterThanOrEqualTo(ValuedCondition):
    pass


class LessThanOrEqualTo(ValuedCondition):
    pass


class Before(ValuedCondition):
    pass


class After(ValuedCondition):
    pass


class OnOrBefore(ValuedCondition):
    pass


class OnOrAfter(ValuedCondition):
    pass


class PastWeek(ObjectCondition):
    pass


class PastMonth(ObjectCondition):
    pass


class PastYear(ObjectCondition):
    pass


class NextWeek(ObjectCondition):
    pass


class NextMonth(ObjectCondition):
    pass


class NextYear(ObjectCondition):
    pass
