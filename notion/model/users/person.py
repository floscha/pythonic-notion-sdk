from notion.model.users import User


class Person(User["Person"]):
    @property
    def email(self) -> str:
        return self._data["person"]["email"]

    @staticmethod
    def from_json(data) -> "Person":
        return Person(data)
