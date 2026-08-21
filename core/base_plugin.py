from config import config
from core.command_manager import CommandManager
from core.database_manager import DatabaseManager


class BasePlugin:
    """
    کلاس پایه برای همه ی پلاگین ها
    """
    name = None
    version = "1.0.0"

    def __init__(
        self,
        client,
        command_manager: CommandManager,
        db: DatabaseManager,
    ):
        self.client = client
        self.command_manager = command_manager
        self.db = db
        self.enabled = False
        self.config = config
        self._event_handlers = []

    def listen(self, event_type):
        """
        دکوریتور برای ثبت هندلر رویداد. برخلاف @self.client.on مستقیم،
        این یکی رو خودش موقع disable پاک می‌کنه، بدون نیاز به کد
        اضافه تو خود پلاگین.

        مثال:
            @self.listen(events.NewMessage(incoming=True))
            async def on_message(event):
                ...
        """
        def decorator(func):
            self.client.add_event_handler(func, event_type)
            self._event_handlers.append((func, event_type))
            return func

        return decorator


    async def cleanup(self):
        """
        همه‌ی هندلرهایی که با self.listen() ثبت شدن رو پاک می‌کنه.
        این رو plugin_manager خودکار موقع disable صدا می‌زنه.
        """
        for func, event_type in self._event_handlers:
            self.client.remove_event_handler(func, event_type)
        self._event_handlers.clear()

    async def on_load(self):
        """
        فقط یک‌بار موقع discover_plugins صدا زده می‌شه.
        جای مناسب برای CREATE TABLE IF NOT EXISTS.
        """
        pass

    async def on_enable(self):
        pass

    async def on_disable(self):
        pass

    def __repr__(self):
        return f"<Plugin {self.name} v{self.version}>"