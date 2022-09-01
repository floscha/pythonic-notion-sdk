from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from notion.api.client import NotionClient


class BaseMixin:
    id: Any
    type: str
    _data: dict
    _client: "NotionClient"
    "Base class for all other mixins that defines which properties should generally be available."
    # @property
    # def id(self) -> str:
    #     return self.id

    # @property
    # def type(self) -> str:
    #     return self.type

    # @property
    # def _data(self) -> dict:
    #     return self._data

    # @_data.setter
    # def _data(self, new_data) -> None:
    #     self._data = new_data

    # @property
    # def _client(self) -> "NotionClient":
    #     return self._client
