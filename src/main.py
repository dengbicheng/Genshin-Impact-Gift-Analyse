from GenshinImpact import GenshinImpact
from RequestThread import RequestThread
import time


# 使用单线程爬取
def singleThread(url):
    start = time.time()
    # 单线程
    a = GenshinImpact(url, 301, save_data=True)
    a.requestData()
    b = GenshinImpact(url, 200, save_data=True)
    b.requestData()
    c = GenshinImpact(url, 302, save_data=True)
    c.requestData()

    # 返回爬取的时间
    return time.time() - start

    # 单线程爬取耗时38秒这里是我的测试数据wait为0.2


# 使用多线程爬取
def multiThreading(url):
    start = time.time()

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

    # 返回爬取的时间
    return time.time() - start


if __name__ == '__main__':

    while True:
        url = input("输入你的链接（输入空格退出程序）：")

        # 输入空格就退出
        if url.strip() == "":
            break

        choose = input("请选择爬取方式【A】单线程爬取，【B】多线程爬取（输入空格退出程序）：")

        # 上面同理
        if choose.strip() == "":
            break

        # 输入的小写转成大写
        choose = choose.upper()

        if choose == 'A':
            time = singleThread(url)
            print('运行时间为：', time)
            break
        elif choose == 'B':
            time = multiThreading(url)
            print('运行时间：', time)
            break
        else:
            print('输入有误，请重新输入！')
