import requests
import time
import json
from MysqlDatabase import MysqlDatabase


class GenshinImpact:
    # 构造函数
    def __init__(self, _url, gacha_type, save_data=False, up_database=False, wait=0.2):
        self.url = _url.split('?')[1].split('#')[0]  # 截取url
        self.kc = gacha_type  # 读取卡池类型参数从外面调取
        self.header = GenshinImpact.openHeader(self)  # 头部标签
        self.page = 1  # 默认页面为一
        self.end_id = 0  # 默认从第一个开始抓取
        self.wait = wait  # 间隔时间
        # 截取URL
        self.get_url = f'https://hk4e-api.mihoyo.com/event/gacha_info/api/getGachaLog?{self.url}&gacha_type={self.kc}&page={self.page}&size=20&end_id={self.end_id}'
        self.arr = []  # 存放数据的列表
        self.up_database = up_database  # 是否上传数据库默认为False
        self.save = save_data  # 是否生成json文件默认为False
        # 这里判断你传进来的是那个卡池，保存文件时会用到
        if self.kc == 200:
            self.kc_name = '常驻池'
        elif self.kc == 301:
            self.kc_name = 'up池'
        elif self.kc == 302:
            self.kc_name = '武器池'

    # 去json文件中拿取头部数据，直接把头部文件写在py文件中也是可以的
    def openHeader(self):
        f = open('header.json', 'r')
        header = json.loads(f.read())['header']
        return header

    # 请求数据
    def requestData(self):

        while True:  # 循环请求数据
            time.sleep(self.wait)  # 延迟爬取，爬取太快会被拦截，使用默认值就好
            self.get_url = f'https://hk4e-api.mihoyo.com/event/gacha_info/api/getGachaLog?{self.url}&gacha_type={self.kc}&page={self.page}&size=20&end_id={self.end_id}'
            response = requests.get(self.get_url, headers=self.header).json()['data']['list']  # 截取返回的json数据
            if len(response) == 0:  # 判断当返回的数据为0时保存数据并返回列表
                if self.save:
                    # 执行保存代码函数
                    GenshinImpact.saveData(self)  # 保存成json文件
                if self.up_database:
                    # 上传数据库
                    GenshinImpact.uploading(self)
                return print(len(self.arr))  # 这里是测试用的，返回可以结束循环，并且打印列表的长度
            print(response)

            for i in response:
                # 格式化数据，这里主要是变成我想要的数据进行保存
                jn = {
                    "uid": i['uid'],
                    "time": i['time'],
                    "name": i['name'],
                    "item_type": i['item_type'],
                    "rank_type": i['rank_type'],
                    "pool_type": i['gacha_type']
                }
                self.arr.append(jn)  # 将数据添加到列表中
            self.page += 1  # 每次爬取一页自动加一
            try:
                self.end_id = response[-1]['id']  # 拿取id，这个id决定了你在哪里开始爬取
            except IndexError:
                break

    # 创建json文件并保存数据
    def saveData(self):
        try:
            time_name = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())  # 格式化时间
            f = open(f'../data/{self.arr[1]["uid"]}_{time_name}_{self.kc_name}.json', 'w',
                     encoding='utf-8')  # 打开一个文件以时间命名
            json.dump(self.arr, f, ensure_ascii=False, indent=0)
        except IndexError as f:
            print(f)

    # 上传数据库
    def uploading(self):
        data = MysqlDatabase()
        data.insert_data(self.arr)
