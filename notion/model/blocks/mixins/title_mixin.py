from .base_mixin import BaseMixin


class TitleMixin(BaseMixin):
    def __init__(self, title: str) -> None:
        title_property_name = self._find_title_property_name()
        self._data["properties"] |= {
            title_property_name: {"title": [{"text": {"content": title}}]}
        }

    def _find_title_property_name(self) -> str:
        """Find the name of the title property for a page.
        While every page must have exactly one title, its name can be changed.
        """
        for property_name, property_dict in self._data["properties"].items():
            if property_dict["type"] == "title":
                return property_name
        raise ValueError(f"Block {self.id!r} has no title property.")

    @property
    def title(self) -> str:
        title_property_name = self._find_title_property_name()
        return self._data["properties"][title_property_name]["title"][0]["text"][
            "content"
        ]

    @title.setter
    def title(self, new_title: str):
        title_property_name = self._find_title_property_name()
        updated_page = self._client.pages.update(
            self.id,
            {
                "properties": {
                    title_property_name: {"title": [{"text": {"content": new_title}}]}
                }
            },
        )
        self._data = updated_page._data
