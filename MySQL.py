#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pymysql

class MyDB:
    global db
    global cursor
    def __init__(self):
        # 打开数据库连接
        global db
        db = pymysql.connect("localhost","root","root","tmall" )
        db.set_charset('utf8')
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')


    def insert(self, sql):
        global db
        global cursor
        # print(sql)
        try:
           # 执行sql语句
            cursor = db.cursor()
            cursor.execute(sql)
           # 提交到数据库执行
            db.commit()
        except:
           # 如果发生错误则回滚
           db.rollback()
           print("db error")

    def select(self, sql):
        global db
        global cursor
        try:
            # 使用 execute()  方法执行 SQL 查询
            cursor.execute(sql)

            # 使用 fetchone() 方法获取单条数据.
            ret = cursor.fetchall()

        except:
            print("db error")
        return ret

    def update(self, sql):
        global db
        global cursor
        try:
           # 执行sql语句
           cursor.execute(sql)
           # 提交到数据库执行
           db.commit()
        except:
           # 如果发生错误则回滚
           db.rollback()
           print("db error")

    def delete(self, sql):
        global db
        global cursor
        try:
           # 执行sql语句
           cursor.execute(sql)
           # 提交到数据库执行
           db.commit()
        except:
           # 如果发生错误则回滚
           db.rollback()
           print("db error")

    def __close__(self):
        global db
        db.close()