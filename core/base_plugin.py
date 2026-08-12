from config import config 

class BasePlugin:
    """
    کلاس پایه برای همه‌ی پلاگین‌ها.
    هر پلاگین باید این کلاس را ارث‌بری کند.
    """

    # اطلاعات پلاگین (اجباری)
    name = None
    version = "1.0.0"


    def __init__(self, client):

        self.client = client
        self.enabled = False
        self.config = config



    def __repr__(self):
        return f"<Plugin {self.name} v{self.version}>"
        