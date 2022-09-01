from notion.model.users import User


class Person(User["Person"]):
    type = "person"

    @property
    def email(self) -> str:
        return self._data["person"]["email"]
