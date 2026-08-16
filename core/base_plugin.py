from config import config


class BasePlugin:
    """
    کلاس پایه برای همه‌ی پلاگین‌ها.
    """

    name = None
    version = "1.0.0"

    def __init__(self, client):
        self.client = client
        self.enabled = False
        self.config = config

    async def on_enable(self):
        """
        زمانی که پلاگین فعال می‌شود اجرا خواهد شد.
        """
        pass

    async def on_disable(self):
        """
        زمانی که پلاگین غیرفعال می‌شود اجرا خواهد شد.
        """
        pass

    def __repr__(self):
        return f"<Plugin {self.name} v{self.version}>"