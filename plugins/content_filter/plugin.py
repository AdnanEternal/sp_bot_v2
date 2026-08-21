from splusthon import events

from core.base_plugin import BasePlugin

from . import handlers
from .commands import register_commands
from .store import WordFilterStore


class ContentFilterPlugin(BasePlugin):
    name = "Content Filter"
    version = "1.0.0"

    def __init__(self, client, command_manager, db):
        super().__init__(client, command_manager, db)
        self.word_filter = WordFilterStore(self.db)

    async def on_load(self):
        await self.word_filter.create_table()

    async def on_enable(self):
        register_commands(self)

        @self.listen(events.NewMessage(incoming=True))
        async def on_message(event):
            await handlers.filter_message(self, event)