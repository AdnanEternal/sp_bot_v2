from collections import defaultdict


class WordFilter:
    """
    فیلتر کلمات به تفکیک هر چت. هر گروه لیست کلمات فیلترشده‌ی
    مستقل خودش رو داره.
    """

    def __init__(self):
        self._words_by_chat: dict[int, set[str]] = defaultdict(set)

    def add(self, chat_id: int, word: str):
        self._words_by_chat[chat_id].add(word.lower())

    def remove(self, chat_id: int, word: str):
        words = self._words_by_chat.get(chat_id)
        if words:
            words.discard(word.lower())

    def contains(self, chat_id: int, text: str) -> bool:
        words = self._words_by_chat.get(chat_id)
        if not words:
            return False

        text = text.lower()
        return any(word in text for word in words)

    def get_all(self, chat_id: int) -> set[str]:
        return self._words_by_chat.get(chat_id, set()).copy()