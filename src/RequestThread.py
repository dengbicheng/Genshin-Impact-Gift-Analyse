import threading
from GenshinImpact import GenshinImpact


# 定义自定义线程类
class RequestThread(threading.Thread):
    def __init__(self, url, gacha_type, save_data=False, up_database=False, wait=1.5):
        threading.Thread.__init__(self)
        self.url = url
        self.gacha_type = gacha_type
        self.save_data = save_data
        self.up_database = up_database
        self.wait = wait

    def run(self):
        genshin_impact = GenshinImpact(self.url, self.gacha_type, save_data=self.save_data,
                                       up_database=self.up_database, wait=self.wait)
        genshin_impact.requestData()
