import pymysql
class MySQL(object):
    """
        定义一个MySQL操作工具类
    """
    def set_conn_info(self, user, password):
        self.__user = user
        self.__password = password
        self.__db = user
    def db_con(self):
        self.conn = pymysql.connect(host="rm-2ze4xo3285lltx27gho.mysql.rds.aliyuncs.com",
                                    port=3306,
                                    user=self.__user,
                                    password=self.__password,
                                    database=self.__db,
                                    autocommit=True)
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)

    def __del__(self):
        if hasattr(self, "cursor"):
            self.cursor.close()
        if hasattr(self, "conn"):
            self.conn.close()
