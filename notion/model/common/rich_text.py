class RichText:
    def __init__(self, text: str):
        self.text = text

    @staticmethod
    def from_json(data: dict) -> "RichText":
        text = data["text"]["content"]
        return RichText(text)

    def to_json(self) -> dict:
        return {
            "type": "text",
            "text": {
                "content": self.text,
            },
        }

    def __str__(self) -> str:
        return self.text

    def __repr__(self) -> str:
        return str(self)
