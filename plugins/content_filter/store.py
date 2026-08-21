class WordFilterStore:
    """
    لایه‌ی persistence فیلتر کلمات. API بیرونی مشابه WordFilter قبلیه
    (add/remove/contains) با این تفاوت که حالا async هستن و روی SQLite کار می‌کنن.
    """

    TABLE = "content_filter_words"

    def __init__(self, db):
        self.db = db

    async def create_table(self):
        await self.db.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.TABLE} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_id INTEGER NOT NULL,
                word TEXT NOT NULL,
                UNIQUE(group_id, word)
            )
        """)
        await self.db.execute(f"""
            CREATE INDEX IF NOT EXISTS idx_{self.TABLE}_group_id
            ON {self.TABLE} (group_id)
        """)

    async def add(self, group_id: int, word: str):
        word = word.lower().strip()
        await self.db.execute(
            f"INSERT OR IGNORE INTO {self.TABLE} (group_id, word) VALUES (?, ?)",
            (group_id, word),
        )

    async def remove(self, group_id: int, word: str):
        word = word.lower().strip()
        await self.db.execute(
            f"DELETE FROM {self.TABLE} WHERE group_id = ? AND word = ?",
            (group_id, word),
        )

    async def contains(self, group_id: int, text: str) -> bool:
        words = await self.get_all(group_id)
        text = text.lower()
        return any(word in text for word in words)

    async def get_all(self, group_id: int) -> set:
        rows = await self.db.fetchall(
            f"SELECT word FROM {self.TABLE} WHERE group_id = ?",
            (group_id,),
        )
        return {row["word"] for row in rows}