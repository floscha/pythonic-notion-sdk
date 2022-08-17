from typing import Union

from notion.model.common.utils import UUIDv4


class Parent:
    """The parent Notion object of another given Notion object.

    Docs: https://developers.notion.com/reference/parent-object
    """

    def __init__(self, type_: str, id_: Union[UUIDv4, str, bool]):
        if isinstance(id_, str) and type_ in ("page_id", "database_id"):
            id_ = UUIDv4(id_)
        elif isinstance(id_, bool) and id_ and type_ == "workspace":
            pass
        else:
            raise ValueError("Invalid combination of `id_` and `type_` arguments.")

        self.type = type_
        self.id = id_

    @staticmethod
    def from_json(
        data: dict,
    ) -> Union["ParentWorkspace", "ParentPage", "ParentDatabase", None]:
        if "parent" not in data:
            return None

        type_ = data["parent"]["type"]
        id_ = data["parent"][type_]

        if type_ == "workspace":
            return ParentWorkspace()
        elif type_ == "page_id":
            return ParentPage(id_)
        elif type_ == "database_id":
            return ParentDatabase(id_)
        else:
            # FIXME: This can never be reached because id_=... line will not find key.
            raise ValueError(f"Parent type {type_!r} is not supported.")

    def to_json(self):
        return {"type": self.type, self.type: self.id}


class ParentWorkspace(Parent):
    def __init__(self):
        super().__init__("workspace", True)


class ParentPage(Parent):
    def __init__(self, id_):
        super().__init__("page_id", id_)


class ParentDatabase(Parent):
    def __init__(self, id_):
        super().__init__("database_id", id_)
