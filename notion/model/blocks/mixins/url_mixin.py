from .base_mixin import BaseMixin


class UrlMixin(BaseMixin):
    def __init__(self, url: str):
        self._data[self.type] |= {"url": url}

    @property
    def url(self) -> str:
        return self._data[self.type]["url"]

    @url.setter
    def url(self, new_url: str):
        new_data = self._client.blocks.update(self.id, {self.type: {"url": new_url}})
        self._data = new_data
