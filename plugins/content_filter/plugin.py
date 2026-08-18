from splusthon import events

from core.base_plugin import BasePlugin

from .commands import register_commands
from .filters import WordFilter


class ContentFilterPlugin(BasePlugin):
    name = "Content Filter"
    version = "1.0.0"

    def __init__(self, client, command_manager):
        super().__init__(client, command_manager)

        self.word_filter = WordFilter()

    async def on_enable(self):
        register_commands(self)

        @self.client.on(events.NewMessage(incoming=True))
        async def filter_message(event):
            
            if self.word_filter.contains(event.raw_text):
                await event.delete()

        self.filter_handler = filter_message

    async def filter_command(self, event):
        text = event.raw_text.strip()

        word = text[len("!فیلتر "):].strip()

        if not word:
            return

        self.word_filter.add(word)

        await event.reply(
            f"کلمه «{word}» به لیست فیلتر اضافه شد."
        )