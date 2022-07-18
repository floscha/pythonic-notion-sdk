from datetime import datetime


def parse_notion_datetime(datetime_str: str) -> datetime:
    "Turn a Notion datetime string into a Python `datetime` object."
    return datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%f%z")


class NotionObjectBase:
    def __init__(self, data=None, client=None):
        self._data = data
        self._client = client

    @property
    def object(self) -> str:
        """Get the Notion object type of the page as a string.

        Takes the value from the page's data while in practice it must always be `"page"`.
        """
        return self._data["object"]

    @property
    def id(self) -> str:
        return self._data["id"]

    @property
    def created_time(self) -> datetime:
        return parse_notion_datetime(self._data["created_time"])

    @property
    def created_by(self) -> dict:
        """Get the user that created the page/block.

        Example: {"object": "user", "id": "45ee8d13-687b-47ce-a5ca-6e2e45548c4b"}
        """
        return self._data["created_by"]

    @property
    def last_edited_time(self) -> datetime:
        return parse_notion_datetime(self._data["last_edited_time"])

    @property
    def last_edited_by(self) -> dict:
        return self._data["created_by"]

    @property
    def archived(self) -> bool:
        return self._data["archived"]

    def to_dict(self) -> dict:
        res = self._data.copy()
        if "children" in res[self.type]:
            res[self.type]["children"] = [
                child.to_dict() for child in res[self.type]["children"]
            ]
        return res
