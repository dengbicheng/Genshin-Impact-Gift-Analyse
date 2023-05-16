# Python获取原神抽卡记录

## 前言：

>
本项目是一个开源的工具，使用Python编程语言开发。通过这个工具，玩家可以自动获取原神游戏中的抽卡记录，包括抽卡时间、获得的角色和武器等信息。该工具使用原神游戏提供的API进行数据获取，并提供了简单易用的命令行界面和数据存储功能。这个项目可以获取你的抽卡记录进行保存到数据库和本地。项目供大家参考学习。

## `GenshinImpact`类【单线程】

```python
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
```

以上代码定义了一个名为`GenshinImpact`的类，并实现了其构造函数`__init__`。以下是对代码的分析和说明：

- `__init__(self, _url, gacha_type, save_data=False, up_database=False, wait=0.2)`
  ：构造函数接受多个参数来初始化`GenshinImpact`类的实例。
- `self.url = _url.split('?')[1].split('#')[0]`：从传入的URL中提取参数部分，并存储在`self.url`中。
- `self.kc = gacha_type`：将传入的`gacha_type`参数存储在`self.kc`中。
- `self.header = GenshinImpact.openHeader(self)`：调用`GenshinImpact`类的`openHeader`
  方法，获取头部标签，并将其存储在`self.header`中。
- `self.page = 1`：将`self.page`初始化为1，表示默认的页面为1。
- `self.end_id = 0`：将`self.end_id`初始化为0，表示默认从第一个数据开始抓取。
- `self.wait = wait`：将传入的`wait`参数存储在`self.wait`中，表示请求的间隔时间，默认为0.2秒。
- `self.get_url =
  f'https://hk4e-api.mihoyo.com/event/gacha_info/api/getGachaLog?{self.url}&gacha_type={self.kc}&page={self.page}&size=20&end_id={self.end_id}'`：构建请求的URL，其中包括了参数信息。
- `self.arr = []`：初始化一个空列表`self.arr`，用于存放数据。
- `self.up_database = up_database`：将传入的`up_database`参数存储在`self.up_database`中，默认为`False`，表示是否上传数据库。
- `self.save = save_data`：将传入的`save_data`参数存储在`self.save`中，默认为`False`，表示是否生成JSON文件保存数据。
- `if self.kc == 200: ...`：根据传入的`gacha_type`参数值，判断卡池的类型，并将对应的名称存储在`self.kc_name`中。

总体而言，这段代码实现了`GenshinImpact`
类的构造函数，用于初始化实例对象时的一些设置和变量赋值。它根据传入的参数初始化了一些实例属性，包括URL参数、卡池类型、请求头、页面、数据存储列表等。同时，根据传入的卡池类型，也设置了相应的卡池名称用于保存文件时的标识。

### 链接分析

这是游戏中获取的链接

```
https://webstatic.mihoyo.com/hk4e/event/e20190909gacha-v2/index.html?win_mode=fullscreen&authkey_ver=1&sign_type=2&auth_appid=webview_gacha&init_type=301&gacha_id=4157ddbd5d5fb886f55ca7b111a3e568e663f3be&timestamp=1677627587&lang=zh-cn&device_type=pc&game_version=CNRELWin3.5.0_R13558307_S13586568_D13586568&plat_type=pc&region=cn_gf01&authkey=d59iXRVJaDE4sM2CEQf4Yw2OzWUb0SsjDOURwdxpkDbyqO9AxxzGoe0RMVn6VjgqSElt4Op5vtlCajh7yLHiLjXf01ZH9EU7fvsSE2CRFuBSoxcZWf31pj3FnGu7jwIBmuRhtTCMxwMrXflRWgYUYK4SoRRokyLNGkYfkajI4LhP2A8SiBkvLbA9ampb3VCImnGkr%2b%2bnIqKjWlQC4qfYdRrnOwOSwsZ%2fuBeLbi8aOCjfO%2bkIXT15cjc%2b%2bnU2IAwZ%2f70VjPkIhMo65xOr58c4iIQl6XDbYbXPHr3sCIz6rv1vLhKpPXe%2byiMkpH%2bXic3niiXtyCkLnzUgar3WHtbGRgr%2b0UWy9GH1rnx0IXk5cGmGk5QOiX8gc%2fd0LkfUexyyqVKbFRbC0LhHkHDOv9dVL2%2fd5epfBDLmVaFsA%2fa8z0qItrJVLFEkFy0MXrzhpZeywIA1cnXEm7XjBa%2bRHcrCNfCtAyMYiO06X62%2bBwbc8ucvERFwYspZmWQpeoOGGawJpkScpz2gSPiM5dlb78kGP0ggXuXgYooVIwX6kQHyRieJFHOF0gMLvjnoMfUos3c3%2f6yH7qjOqmv8YFAFCcMTetT2Lv7%2by9rNUXJYA0W5hf4qrWU4lST0uO%2fNrbUajiXT6EuJp30mGWKAZpZbOUFFoW3XhbaZRaw%2fzieWMBQZX1Jf60ihViruEToFja9d5FHzEDaxZ7mgbKOAG%2fzPGhuZ6gQKLij%2bEDFS%2fbA5T8NtTfcYVhhJW0lPLbuofwcJz7VUArkvm37T1NfQ9AZJQCfal5xe061DTFtCYQ2J9uNTG6RJjDFEl0iRuZT4qYJBUsbAsCH1pn1BbWJCbflpRvdQBZOvDvOz4d6itn7K2JheDZks5DoC1sn0YKmuiWhfN2V50X11227kqCdTlaIgSQ7yhr%2faeR2dJIIEmK8aTsm5JfW%2fBvkQzwCkekT4v1PPL8KhlaEgy3lrPme4SQmBlzBOt28lRCRfnEZ3BbrU8L0TjwsTRTcdHtjbq39oIJiRQ%2brJtvsU8%2b8iSuo75K52UrQ27onJIg5rCw6tHJvC%2fffBAa8JptMgJrLfzxjDUsVqrzq6xntkyoCziwB3%2fp9rjpY4lUyMjs9GwyQzeUEcE%2bqkjBoumuQfK9iDmlZftOdgK0zNFMkO8170M8CwFEcWc524NcR621ak7PCToKDjaA1gyuOJQvDI6htjN67jZB0Jp4KE2Rw6%2bxa5HcBsySxL8Lo%2bce0pe%2fiRWMZZ3Tt9KViVNp7LY8a2pgNejz6B1HMu8zSSNGixFZyLJR50RdtEOaErCwU4TBJbmUNrVyJNplb4%2fIYOPLrVWurx9DwE9WzwfF2zf4J0YH446frz9T2NqOwlGg%3d%3d&game_biz=hk4e_cn#/log
```

这是请求数据的URL

```
https://hk4e-api.mihoyo.com/event/gacha_info/api/getGachaLog?win_mode=fullscreen&authkey_ver=1&sign_type=2&auth_appid=webview_gacha&init_type=301&gacha_id=4157ddbd5d5fb886f55ca7b111a3e568e663f3be&timestamp=1677627587&lang=zh-cn&device_type=pc&game_version=CNRELWin3.5.0_R13558307_S13586568_D13586568&plat_type=pc&region=cn_gf01&authkey=d59iXRVJaDE4sM2CEQf4Yw2OzWUb0SsjDOURwdxpkDbyqO9AxxzGoe0RMVn6VjgqSElt4Op5vtlCajh7yLHiLjXf01ZH9EU7fvsSE2CRFuBSoxcZWf31pj3FnGu7jwIBmuRhtTCMxwMrXflRWgYUYK4SoRRokyLNGkYfkajI4LhP2A8SiBkvLbA9ampb3VCImnGkr%2b%2bnIqKjWlQC4qfYdRrnOwOSwsZ%2fuBeLbi8aOCjfO%2bkIXT15cjc%2b%2bnU2IAwZ%2f70VjPkIhMo65xOr58c4iIQl6XDbYbXPHr3sCIz6rv1vLhKpPXe%2byiMkpH%2bXic3niiXtyCkLnzUgar3WHtbGRgr%2b0UWy9GH1rnx0IXk5cGmGk5QOiX8gc%2fd0LkfUexyyqVKbFRbC0LhHkHDOv9dVL2%2fd5epfBDLmVaFsA%2fa8z0qItrJVLFEkFy0MXrzhpZeywIA1cnXEm7XjBa%2bRHcrCNfCtAyMYiO06X62%2bBwbc8ucvERFwYspZmWQpeoOGGawJpkScpz2gSPiM5dlb78kGP0ggXuXgYooVIwX6kQHyRieJFHOF0gMLvjnoMfUos3c3%2f6yH7qjOqmv8YFAFCcMTetT2Lv7%2by9rNUXJYA0W5hf4qrWU4lST0uO%2fNrbUajiXT6EuJp30mGWKAZpZbOUFFoW3XhbaZRaw%2fzieWMBQZX1Jf60ihViruEToFja9d5FHzEDaxZ7mgbKOAG%2fzPGhuZ6gQKLij%2bEDFS%2fbA5T8NtTfcYVhhJW0lPLbuofwcJz7VUArkvm37T1NfQ9AZJQCfal5xe061DTFtCYQ2J9uNTG6RJjDFEl0iRuZT4qYJBUsbAsCH1pn1BbWJCbflpRvdQBZOvDvOz4d6itn7K2JheDZks5DoC1sn0YKmuiWhfN2V50X11227kqCdTlaIgSQ7yhr%2faeR2dJIIEmK8aTsm5JfW%2fBvkQzwCkekT4v1PPL8KhlaEgy3lrPme4SQmBlzBOt28lRCRfnEZ3BbrU8L0TjwsTRTcdHtjbq39oIJiRQ%2brJtvsU8%2b8iSuo75K52UrQ27onJIg5rCw6tHJvC%2fffBAa8JptMgJrLfzxjDUsVqrzq6xntkyoCziwB3%2fp9rjpY4lUyMjs9GwyQzeUEcE%2bqkjBoumuQfK9iDmlZftOdgK0zNFMkO8170M8CwFEcWc524NcR621ak7PCToKDjaA1gyuOJQvDI6htjN67jZB0Jp4KE2Rw6%2bxa5HcBsySxL8Lo%2bce0pe%2fiRWMZZ3Tt9KViVNp7LY8a2pgNejz6B1HMu8zSSNGixFZyLJR50RdtEOaErCwU4TBJbmUNrVyJNplb4%2fIYOPLrVWurx9DwE9WzwfF2zf4J0YH446frz9T2NqOwlGg%3d%3d&game_biz=hk4e_cn&
gacha_type=301&
page=1&
size=5&
begin_id=1677117960001223732
```

通过对比和游戏中的链接有以下不同需要

```
https://hk4e-api.mihoyo.com/event/gacha_info/api/getGachaLog?
gacha_type=301&
page=1&
size=6&
end_id=0
```

- `gacha_type`代表卡池信息 新手卡池为100 ，常驻卡池为200，up卡池为301 ，武器卡池为302
- `page`代表页数
- `size`代表请求多少条数据最多20条
- `end_id`
  这个参数很重要，这个参数表示从什么地方开始查询数据，不携带这个参数会从最前面的第一个开始查起，每次最多只能查询20条数据也就是说没有这个参数你就只能查询最前面的20条数据，但是每次查询时返回的数据中都会携带查询下一次的id所以不用慌

### requestData方法获取抽卡记录

```python
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
```

以上代码是一个名为`requestData`的方法，看起来是一个用于请求数据的循环。下面是对代码的分析和作用说明：

- `while True:`：无限循环，用于持续请求数据。
- `time.sleep(self.wait)`: 使用`self.wait`参数定义的时间间隔进行延迟，以便控制爬取速度。
- `self.get_url`：构建请求的URL。
- `response = requests.get(self.get_url, headers=self.header).json()['data']['list']`
  ：发送GET请求到指定URL，获取返回的JSON数据，并从中提取出键为`'data'`，其值中的键为`'list'`的数据。
- `if len(response) == 0:`：检查返回的数据是否为空列表。
    - 如果数据为空列表，执行以下操作：
        - 如果`self.save`为`True`，调用`GenshinImpact.saveData(self)`函数进行数据保存（以JSON文件的形式）。
        - 如果`self.up_database`为`True`，调用`GenshinImpact.uploading(self)`函数进行数据上传。
        - 返回列表`self.arr`的长度，并打印。
- `print(response)`：打印响应数据。
- `for i in response:`：遍历响应数据中的每个元素。
- `jn = { ... }`：将数据格式化为所需的格式，并将其存储在字典`jn`中。
- `self.arr.append(jn)`：将格式化后的数据字典`jn`添加到列表`self.arr`中。
- `self.page += 1`：自增`self.page`的值，以便爬取下一页数据。
- `self.end_id = response[-1]['id']`：获取响应数据最后一个元素的`'id'`字段的值，用于确定下一次爬取的起始位置。
- `except IndexError: break`：如果发生`IndexError`异常（例如，响应数据已经没有更多元素），跳出循环。

总体而言，这段代码的作用是通过不断发送请求来获取原神抽卡记录数据。每次请求获取到的数据会进行格式化，并添加到列表`self.arr`
中，直到没有更多数据可获取为止。根据条件设置，可以选择保存数据到JSON文件或上传到数据库。

## `RequestThread`类【多线程】

**这个类用于多线程爬取**

```python
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

```

以上代码实现了一个使用多线程进行数据请求的程序。

- `import threading`: 导入线程模块，用于创建和管理线程。
- `import time`: 导入时间模块，用于计算程序的执行时间。
- `from GenshinImpact import GenshinImpact`: 导入自定义的`GenshinImpact`类，用于进行数据请求。

下面是对代码的分析和说明：

- `class RequestThread(threading.Thread)`: 定义了一个继承自`threading.Thread`的自定义线程类`RequestThread`。
    - `def __init__(self, url, gacha_type, save_data=False, up_database=False, wait=1.5)`: 线程类的构造函数，接收多个参数用于初始化线程。
        - `self.url = url`: 存储传入的URL。
        - `self.gacha_type = gacha_type`: 存储传入的卡池类型。
        - `self.save_data = save_data`: 是否保存数据，默认为`False`。
        - `self.up_database = up_database`: 是否上传数据库，默认为`False`。
        - `self.wait = wait`: 请求的间隔时间，默认为1.5秒。
    - `def run(self)`: 线程的运行方法，会在线程启动后自动执行。
        - `genshin_impact = GenshinImpact(...)`: 创建一个`GenshinImpact`对象，传入相应的参数进行初始化。
        - `genshin_impact.requestData()`: 调用`requestData`方法，开始请求数据。
- `if __name__ == '__main__':`: 程序的入口点，用于判断是否作为主程序运行。
    - `start = time.time()`: 记录程序开始执行的时间。
    - `url = input("输入你要分析的链接：")`: 通过用户输入获取要分析的链接。
    - 创建三个线程对象，并传入不同的卡池类型和其他参数：
        - `thread_a = RequestThread(url, 301, save_data=True)`
        - `thread_b = RequestThread(url, 200, save_data=True)`
        - `thread_c = RequestThread(url, 302, save_data=True)`
    - 启动线程：
        - `thread_a.start()`
        - `thread_b.start()`
        - `thread_c.start()`
    - 等待所有线程完成：
        - `thread_a.join()`
        - `thread_b.join()`
        - `thread_c.join()`
    - `print("耗时：", time.time() - start)`: 打印程序执行的总耗时。
    - 最后的注释`# 多线程28秒这里是我的测试数据wait为1.5`表示作者进行测试时的执行时间和设置的等待时间。

总体而言，这段代码实现了使用多线程进行数据请求的功能。通过创建多个线程对象，并传入不同的卡池类型和其他参数，实现了同时请求多个卡池的数据。每个线程内部创建了一个`GenshinImpact`
对象，并调用其`requestData`方法来请求数据。通过多线程的并发执行，可以提高数据

请求的效率。

## MysqlDatabase 类【上传数据库】

**这个类用于上传数据库**

```python
import pymysql


class MysqlDatabase:

    # 构造函数
    def __init__(self):
        data = {
            'host': 'localhost',  # 数据库地址
            'port': 3306,  # 数据库端口
            'user': 'root',  # 数据库用户名
            'password': '123456789',  # 密码
            'db': 'genshin_impact',  # 数据库名称
            'charset': 'utf8'  # 编码格式
        }
        # 连接数据库
        self.db = pymysql.connect(**data)
        print("连接成功")
        # 创建游标
        self.cursor = self.db.cursor()
        print('游标创建成功')

        # 插入数据

    def insert_data(self, sj):
        # f = open('../data/20230403094235-up池.json', 'r', encoding='utf-8')
        # sj = json.loads(f.read())
        for i in sj:
            sql = """
                   INSERT INTO record(uid, grab_time, goods_name, item_type, rank_type, pool_type)
                   VALUES (%s, %s, %s, %s, %s, %s)
                   """
            records = [(i['uid'], i['time'], i['name'], i['item_type'], i['rank_type'], i['pool_type']) for i in sj]
            # 使用 executemany() 执行 SQL
            # executemany 方法用于一次性插入多个记录，可以减少与数据库的交互次数，提高效率。
            self.cursor.executemany(sql, records)

        print('插入完毕')

        # 提交到数据库执行
        self.db.commit()
        # 关闭数据库连接
        self.db.close()
        print('数据库已关闭')
```

以上代码定义了一个名为`MysqlDatabase`的类，用于连接MySQL数据库并插入数据。

下面是对代码的分析和说明：

- `import pymysql`: 导入pymysql模块，用于连接和操作MySQL数据库。
- `class MysqlDatabase`: 定义了一个名为`MysqlDatabase`的类。
    - `def __init__(self)`: 构造函数，用于连接数据库和创建游标。
        - `data = {...}`: 定义了数据库连接所需的参数，包括主机地址、端口号、用户名、密码、数据库名称和编码格式。
        - `self.db = pymysql.connect(**data)`: 使用`pymysql.connect()`函数连接数据库，并将连接对象存储在`self.db`中。
        - `self.cursor = self.db.cursor()`: 创建游标对象，用于执行SQL语句，并将其存储在`self.cursor`中。
    - `def insert_data(self, sj)`: 插入数据方法，接收一个数据列表作为参数。
        - `for i in sj: ...`: 遍历数据列表，对每个数据执行插入操作。
        - `sql = "...INSERT INTO record(uid, grab_time, goods_name, item_type, rank_type, pool_type)..."`:
          定义插入数据的SQL语句，使用占位符 `%s` 表示待插入的值。
        - `records = [...]`: 构建记录的列表，每个记录是一个包含数据值的元组，用于批量插入数据。
        - `self.cursor.executemany(sql, records)`: 使用游标对象的`executemany()`方法批量执行插入操作，将SQL语句和数据列表作为参数。
        - `self.db.commit()`: 提交事务，将插入操作真正应用到数据库。
        - `self.db.close()`: 关闭数据库连接。

总体而言，这段代码定义了一个`MysqlDatabase`类，用于连接MySQL数据库并插入数据。在构造函数中，使用`pymysql.connect()`
函数连接数据库，并创建游标对象。插入数据方法`insert_data()`接收一个数据列表作为参数，使用`executemany()`
方法批量执行插入操作，并通过`commit()`方法提交事务。最后，在插入完毕后关闭数据库连接。

请注意，这段代码中的数据库连接信息（如主机地址、用户名、密码）是示例信息，实际使用时需要根据自己的数据库配置进行修改。另外，为了安全起见，不建议将数据库密码直接硬编码在代码中，可以通过配置文件等方式进行存储和读取。



