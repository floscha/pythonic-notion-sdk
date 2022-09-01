from notion.model.users import Bot, Person, User


def test_creating_bot_from_json():
    json_data = {
        "avatar_url": None,
        "bot": {},
        "id": "00000000-1111-2222-3333-444444444444",
        "name": "some_bot",
        "object": "user",
        "type": "bot",
    }

    bot = User.from_json(json_data)

    assert isinstance(bot, Bot)
    assert bot.type == "bot"
    assert bot.id == "00000000-1111-2222-3333-444444444444"
    assert bot.name == "some_bot"
    assert bot.avatar_url is None


def test_creating_person_from_json():
    json_data = {
        "avatar_url": None,
        "id": "00000000-1111-2222-3333-444444444444",
        "name": "Ivan Zhao",
        "object": "user",
        "person": {"email": "some.mail@notion.so"},
        "type": "person",
    }

    person = User.from_json(json_data)

    assert isinstance(person, Person)
    assert person.type == "person"
    assert person.id == "00000000-1111-2222-3333-444444444444"
    assert person.name == "Ivan Zhao"
    assert person.avatar_url is None
