# core/client.py
import os
from splusthon import SoroushClient
from splusthon.sessions import StringSession

class ClientManager:


    def __init__(self, session_string: str = None):

        self.session_string = session_string or os.getenv("SESSION_STRING")
        if not self.session_string:
            raise ValueError("❌ SESSION_STRING یافت نشد! لطفاً آن را در فایل .env تنظیم کنید.")

        self.client = None  # نمونه‌ی کلاینت سروش

    async def start(self):

        try:
            self.client = SoroushClient(StringSession(self.session_string))
            await self.client.start()
            print("✅ ربات به سروش متصل شد.")
            return self.client
        except Exception as e:
            
            print(f"❌ خطا در اتصال به سروش: {e}")
            return None

    async def stop(self):
        """
        اتصال را به‌صورت امن می‌بندد.
        """
        if self.client:
            await self.client.disconnect()
            print("🔌 اتصال به سروش قطع شد.")

    def get_client(self):
        """
        نمونه‌ی کلاینت را برمی‌گرداند (برای استفاده در پلاگین‌ها).
        """
        return self.client