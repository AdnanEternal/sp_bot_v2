import asyncio
from core.client import ClientManager
from config import config
from core.base_plugin import BasePlugin

async def main():

    session_string = config.get_required("SESSION_STRING")

    client = ClientManager(session_string=session_string)
    
    client = await client.start()
    if not client:
        print("❌ برنامه به دلیل عدم اتصال خاتمه می‌یابد.")
        return

    print("⏳ ربات در حال انتظار برای رویدادهاست...")

    try:

        await client.run_until_disconnected()
    except KeyboardInterrupt:
        print("\n🛑 دریافت سیگنال قطع...")
    finally:
        # قطع امن اتصال
        await client.stop()

asyncio.run(main())