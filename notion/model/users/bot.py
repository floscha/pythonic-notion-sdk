from notion.model.users import User


class Bot(User["Bot"]):
    @staticmethod
    def from_json(data) -> "Bot":
        return Bot(data)
