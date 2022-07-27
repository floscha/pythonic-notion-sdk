class Emoji:
    def __init__(self, emoji: str):
        self.emoji = emoji

    def to_json(self) -> dict:
        return {"type": "emoji", "emoji": self.emoji}
