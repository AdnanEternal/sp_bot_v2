import importlib.util
import inspect
from pathlib import Path

from core.base_plugin import BasePlugin


class PluginManager:
    def __init__(self, client):
        self.client = client
        self.plugins = {}

    def discover_plugins(self, plugins_dir="plugins"):
        """
        پلاگین‌ها را از پوشه‌ی plugins پیدا می‌کند.

        ساختار مورد انتظار:

        plugins/
        ├── plugin_a/
        │   └── plugin.py
        ├── plugin_b/
        │   └── plugin.py
        """

        plugins_path = Path(plugins_dir)

        if not plugins_path.exists():
            print(f"⚠️ پوشه‌ی {plugins_dir} وجود ندارد!")
            return

        if not plugins_path.is_dir():
            print(f"❌ مسیر {plugins_dir} یک پوشه نیست!")
            return

        for plugin_folder in plugins_path.iterdir():
            if not plugin_folder.is_dir():
                continue

            plugin_file = plugin_folder / "plugin.py"

            if not plugin_file.exists():
                print(
                    f"⚠️ فایل plugin.py در پلاگین "
                    f"'{plugin_folder.name}' پیدا نشد."
                )
                continue

            plugin_class = self._find_plugin_class(
                plugin_file,
                plugin_folder.name
            )

            if plugin_class is None:
                continue

            try:
                plugin_instance = plugin_class(self.client)

                plugin_name = plugin_instance.name

                if not plugin_name:
                    plugin_name = plugin_folder.name

                if plugin_name in self.plugins:
                    print(
                        f"⚠️ پلاگین '{plugin_name}' قبلاً ثبت شده است."
                    )
                    continue

                self.plugins[plugin_name] = plugin_instance

                print(
                    f"✅ پلاگین '{plugin_name}' "
                    f"v{plugin_instance.version} بارگذاری شد."
                )

            except Exception as e:
                print(
                    f"❌ خطا در ساخت پلاگین "
                    f"'{plugin_folder.name}': {e}"
                )

    def _find_plugin_class(self, plugin_file: Path, module_name: str):
        """
        فایل plugin.py را import می‌کند و کلاس ارث‌بری‌شده
        از BasePlugin را پیدا می‌کند.
        """

        try:
            spec = importlib.util.spec_from_file_location(
                module_name,
                plugin_file
            )

            if spec is None or spec.loader is None:
                print(
                    f"❌ امکان ساخت module برای "
                    f"'{module_name}' وجود ندارد."
                )
                return None

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

        except Exception as e:
            print(
                f"❌ خطا در import پلاگین "
                f"'{module_name}': {e}"
            )
            return None

        plugin_classes = []

        for _, obj in inspect.getmembers(module, inspect.isclass):
            if (
                issubclass(obj, BasePlugin)
                and obj is not BasePlugin
                and obj.__module__ == module.__name__
            ):
                plugin_classes.append(obj)

        if not plugin_classes:
            print(
                f"⚠️ هیچ کلاس پلاگینی در "
                f"'{module_name}' پیدا نشد."
            )
            return None

        if len(plugin_classes) > 1:
            print(
                f"⚠️ در پلاگین '{module_name}' بیش از یک "
                f"کلاس BasePlugin پیدا شد."
            )
            return None

        return plugin_classes[0]

    async def load_all_plugins(self, plugins_dir="plugins"):
        """
        تمام پلاگین‌ها را پیدا و بارگذاری می‌کند.
        """

        self.discover_plugins(plugins_dir)

        print(
            f"📦 تعداد پلاگین‌های بارگذاری‌شده: "
            f"{len(self.plugins)}"
        )

    def get_plugin(self, name):
        """
        دریافت یک پلاگین بر اساس نام.
        """
        return self.plugins.get(name)

    def get_all_plugins(self):
        """
        دریافت تمام پلاگین‌های بارگذاری‌شده.
        """
        return self.plugins.values()

    async def enable_plugin(self, name):
        """
        فعال کردن یک پلاگین.
        """

        plugin = self.get_plugin(name)

        if plugin is None:
            print(f"⚠️ پلاگین '{name}' پیدا نشد.")
            return False

        if plugin.enabled:
            return True

        if hasattr(plugin, "on_enable"):
            result = plugin.on_enable()

            if inspect.isawaitable(result):
                await result

        plugin.enabled = True

        print(f"✅ پلاگین '{name}' فعال شد.")
        return True

    async def disable_plugin(self, name):
        """
        غیرفعال کردن یک پلاگین.
        """

        plugin = self.get_plugin(name)

        if plugin is None:
            print(f"⚠️ پلاگین '{name}' پیدا نشد.")
            return False

        if not plugin.enabled:
            return True

        if hasattr(plugin, "on_disable"):
            result = plugin.on_disable()

            if inspect.isawaitable(result):
                await result

        plugin.enabled = False

        print(f"🛑 پلاگین '{name}' غیرفعال شد.")
        return True

    async def enable_all_plugins(self):
        """
        فعال کردن تمام پلاگین‌ها.
        """

        for name in self.plugins:
            await self.enable_plugin(name)

    async def disable_all_plugins(self):
        """
        غیرفعال کردن تمام پلاگین‌ها.
        """

        for name in list(self.plugins.keys()):
            await self.disable_plugin(name)