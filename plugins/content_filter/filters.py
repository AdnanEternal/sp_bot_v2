class WordFilter:
    def __init__(self):
        self.words = set()

    def add(self, word: str):
        self.words.add(word.lower())

    def remove(self, word: str):
        self.words.discard(word.lower())

    def contains(self, text: str):
        text = text.lower()

        return any(
            word in text
            for word in self.words
        )

    def get_all(self):
        return self.words.copy()