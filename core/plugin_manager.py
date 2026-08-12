import importlib
import inspect
from pathlib import Path



class PluginManager:
    def __init__(self, client):
        self.client = client
        self.plugins = {}

    def discover_plugins(self, plugins_dir="plugins"):
        """
        پوشه‌ی پلاگین‌ها رو اسکن می‌کنه و همه‌ی کلاس‌های ارث‌بری از BasePlugin رو پیدا می‌کنه.
        """
        plugins_path = Path(plugins_dir)

        if not plugins_path.exists():
            print(f"⚠️ پوشه‌ی {plugins_dir} وجود ندارد!")
            return
        for plugin_folder in plugins_path.iterdir():
            if not plugin_folder.is_dir():
                continue  # فقط پوشه‌ها رو بررسی کن

            plugin_file = plugin_folder / "plugin.py"
            if not plugin_file.exists():
                print(f"⚠️ فایل plugin.py در {plugin_folder} پیدا نشد.")
                continue
            print(f"✅ پلاگین '{plugin_folder.name}' پیدا شد.")

    async def load_all_plugins(self):
        """
        همه‌ی پلاگین‌هایی که کشف شدن رو بارگذاری کن.
        """
        # اول باید discover رو صدا زده باشی تا لیستشون رو داشته باشی
        # ولی فعلاً فرض می‌کنیم که پلاگین‌ها رو خودمون می‌دونیم

        # اینجا می‌تونیم پلاگین‌ها رو از یک لیست ثابت یا از کشف شده‌ها بگیریم
        # بعداً که کشف رو کامل کردیم، ازش استفاده می‌کنیم
        pass