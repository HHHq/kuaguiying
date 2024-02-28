import pymysql

"""
链接mysql
"""


class DbHandler:
    # 初始化游标对象
    def __init__(self, database, host, user, password, port):
        self.conn = pymysql.connect(host=host,
                                    user=user,
                                    password=password,
                                    port=port,
                                    database=database,
                                    )
        self.cursor = self.conn.cursor()

    def query(self, query_db_sql, one=True):
        # 执行语句
        self.cursor.execute(query_db_sql)
        # 查询数据
        if one:
            query_data = self.cursor.fetchone()
            return query_data
        query_data_all = self.cursor.fetchall()
        return query_data_all

    def update(self, update_sql):
        self.cursor.execute(update_sql)
        # 提交事务
        self.conn.commit()

    def close(self):
        # 关闭游标，链接
        self.cursor.close()
        self.conn.close()




