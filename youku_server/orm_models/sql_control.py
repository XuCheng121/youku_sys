# Author: Mr.Xu
# @Time : 2019/10/9 8:26

import pymysql

class MySQL:
    sql_obj = None
    def __new__(cls, *args, **kwargs):
        if not cls.sql_obj:
            cls.sql_obj = object.__new__(cls)
        return cls.sql_obj

    def __init__(self):
        self.mysql = pymysql.connect(
            host = "localhost",
            port = 3306,
            user="root",
            passwd="123",
            db="orm_demo",
            charset="utf8",
            autocommit=True

        )
        self.cursor = self.mysql.cursor(pymysql.cursors.DictCursor)

    def select(self,sql,args=None):
        print(sql,"\n",args)
        self.cursor.execute(sql,args)
        res = self.cursor.fetchall()
        return res

    def execute(self,sql,args=None):
        print(sql,"\n",args)
        self.cursor.execute(sql,args)

    def close(self):
        self.cursor.close()
        self.mysql.close()