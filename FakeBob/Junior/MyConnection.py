import pymysql

# 数据库封装
class MysqlConnection(object):
    def __init__(self, host, user, password, database):
        '''
        :param host: IP
        :param user: 用户名
        :param password: 密码
        :param port: 端口号
        :param database: 数据库名
        :param charset: 编码格式
        '''
        self.db = pymysql.connect(host='offline-tech.ikunchi.com',
                                  user = "bi_pro",
                                  passwd = 'EpKgKepLOFdVeClk',
                                  port = 43005,
                                  db = 'ods',
                                  charset='utf8')
        self.cursor = self.db.cursor()
        # 将要插入的数据写成元组传入
        def select(self,sql):
            # 执行SQL语句
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            for row in results:
                print(row)
