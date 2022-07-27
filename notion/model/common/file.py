class File:
    def __init__(self, url: str):
        self.url = url

    def to_json(self) -> dict:
        return {"type": "external", "external": {"url": self.url}}
