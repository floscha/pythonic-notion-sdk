from .child import Child


class ChildDatabase(Child):
    "A database contained in another page."

    def delete(self):
        """Delete the `ChildDatabase` in Notion.

        Needs to be overwritten to use the `delete_database` endpoint instead of `delete_block`.
        """
        deletion_result = self._client.databases.delete(self.id)
        self._data["archived"] = deletion_result["archived"]
