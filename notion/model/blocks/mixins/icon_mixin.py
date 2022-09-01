from typing import Optional, Union

from notion.model.properties.emoji import Emoji
from notion.model.properties.file import File

from .base_mixin import BaseMixin


class IconMixin(BaseMixin):
    def __init__(self, icon: Union[str, Emoji, File]) -> None:
        icon_dict = (
            icon.to_json()
            if isinstance(icon, (Emoji, File))
            else {"emoji": icon, "type": "emoji"}
        )
        self._data[self.type] |= {"icon": icon_dict}

    @property
    def icon(self) -> Optional[str]:
        "TODO: Implement setter"
        icon_dict = self._data[self.type].get("icon")
        if icon_dict is None:
            return None
        elif "emoji" in icon_dict:
            return icon_dict["emoji"]
        else:
            raise NotImplementedError("`File Object` icons are not implemented yet.")

    @icon.setter
    def icon(self, new_icon: str):
        new_data = self._client.blocks.update(
            self.id, {self.type: {"icon": {"emoji": new_icon}}}
        )
        self._data = new_data
