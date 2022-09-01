from notion.model.users import User


class Bot(User["Bot"]):
    type = "bot"
