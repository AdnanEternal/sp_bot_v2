from splusthon import events

from core.base_plugin import BasePlugin

from . import handlers
from .commands import register_commands
from .filters import WordFilter


class ContentFilterPlugin(BasePlugin):
    name = "Content Filter"
    version = "1.1.0"

    def __init__(self, client, command_manager):
        super().__init__(client, command_manager)
        self.word_filter = WordFilter()

    async def on_enable(self):
        register_commands(self)

        @self.listen(events.NewMessage(incoming=True))
        async def on_message(event):
            await handlers.filter_message(self, event)