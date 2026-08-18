from config import config
from core.command_manager import CommandManager


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
    ):
        self.client = client
        self.command_manager = command_manager
        self.enabled = False
        self.config = config

    async def on_enable(self):
        pass

    async def on_disable(self):
        pass

    def __repr__(self):
        return f"<Plugin {self.name} v{self.version}>"