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

        # 查询用户所有抽卡记录语句
        # 下面代码并没有调用
