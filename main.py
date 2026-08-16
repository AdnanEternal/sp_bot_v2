import asyncio

from config import config
from core.client import ClientManager
from core.plugin_manager import PluginManager


async def main():

    session_string = config.get_required("SESSION_STRING")

    client_manager = ClientManager(session_string=session_string)
    
    client = await client_manager.start()

    if not client:
        print("❌ برنامه به دلیل عدم اتصال خاتمه می‌یابد.")
        return

    plugin_manager = PluginManager(client)

    try:
        await plugin_manager.load_all_plugins()
        await plugin_manager.enable_all_plugins()

        print("⏳ ربات در حال انتظار برای رویدادهاست...")

        await client.run_until_disconnected()

    except KeyboardInterrupt:
        print("\n🛑 دریافت سیگنال قطع...")

    finally:
        await plugin_manager.disable_all_plugins()
        await client_manager.stop()


asyncio.run(main())