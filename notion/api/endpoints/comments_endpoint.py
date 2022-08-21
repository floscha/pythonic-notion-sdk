from typing import TYPE_CHECKING, Union

from notion.model.comment import Comment
from notion.model.common.utils import UUIDv4

if TYPE_CHECKING:
    from notion.api.client import NotionClient


class CommentsEndpoint:
    def __init__(self, client: "NotionClient"):
        self._client = client

    def get(self, block_id: Union[UUIDv4, str]) -> list[Comment]:
        data = self._client._paginate("get", "comments", params={"block_id": block_id})
        return [
            Comment.from_json(comment_data).with_client(self._client)
            for comment_data in data
        ]

    def create(self, comment: Comment) -> Comment:
        data = self._client._make_request(
            "post",
            "comments",
            payload=comment.to_json(),
        )
        return Comment.from_json(data)

    def delete(self, comment_id: Union[UUIDv4, str]):
        raise NotImplementedError(
            "The Notion API does not allow deleting comments (yet)."
        )
