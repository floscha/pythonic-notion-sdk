from .child import Child


class ChildPage(Child["ChildPage"]):
    """A page contained in another page.

    From the Notion docs (https://developers.notion.com/docs/working-with-page-content#modeling-content-as-blocks):
        When a child page appears inside another page, it's represented as a `child_page` block, which does not have children.
        You should think of this as a reference to the page block.
    """

    type = "child_page"

    def delete(self):
        """Delete the `ChildPage` in Notion.

        Needs to be overwritten to use the `delete_page` endpoint instead of `delete_block`.
        """
        deletion_result = self._client.pages.delete(self.id)
        self._data["archived"] = deletion_result.archived
