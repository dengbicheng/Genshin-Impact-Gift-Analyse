import threading
import time
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


if __name__ == '__main__':
    start = time.time()
    url = input("输入你要分析的链接：")
    # 创建线程对象
    thread_a = RequestThread(url, 301, save_data=True)
    thread_b = RequestThread(url, 200, save_data=True)
    thread_c = RequestThread(url, 302, save_data=True)

    # 启动线程
    thread_a.start()
    thread_b.start()
    thread_c.start()

    # 等待所有线程完成
    thread_a.join()
    thread_b.join()
    thread_c.join()

    print("耗时：", time.time() - start)

    # 多线程28秒这里是我的测试数据wait为1.5
