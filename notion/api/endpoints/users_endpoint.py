from typing import TYPE_CHECKING, List

from notion.model.users import Bot, User

if TYPE_CHECKING:
    from notion.api.client import NotionClient


class UsersEndpoint:
    def __init__(self, client: "NotionClient"):
        self._client = client

    def get(self, user_id: str) -> User:
        """Get a Notion user based on its user ID.

        Docs: https://developers.notion.com/reference/get-user
        """
        data = self._client._make_request("get", f"users/{user_id}")
        return User.from_json(data).with_client(self._client)

    def get_all(self) -> List[User]:
        """Get a list of all Notion users for the current workspace.

        Docs: https://developers.notion.com/reference/get-users
        """
        data = self._client._paginate("get", "users")
        return [
            User.from_json(user_data).with_client(self._client) for user_data in data
        ]

    def get_token_owner(self) -> Bot:
        """Get the Bot object that owns the used Notion Integration.

        Docs: https://developers.notion.com/reference/get-self
        """
        data = self._client._make_request("get", "users/me")
        bot = Bot.from_json(data).with_client(self._client)
        assert isinstance(bot, Bot)
        return bot
