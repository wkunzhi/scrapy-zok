# -*- coding: utf-8 -*-
# __author__ = "zok" 
# Date: 2019/3/7  Python: 3.7

import pymysql

from zok.zok_config import *
from zok.repetition.update_cache import CacheRedis


class SaveToMysqlBase(object):
    """
    mysql储存基类
    新增语法 INSERT INTO 表名(city, county, district) VALUES ("%s","%s","%s")
    更新语法 UPDATE 表名 SET mail = "playstation.com" WHERE user_name = "Peter"
    """
    conn = None
    cursor = None  # 游标对象
    redis = CacheRedis()

    # 1. 链接数据库
    # 2. 执行sql语句
    # 3. 提交

    # 爬虫开始执行
    def open_spider(self, spider):
        print('开始爬虫，链接数据库')
        self.conn = pymysql.Connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            db=MYSQL_DB_NAME,
        )

    def process_item(self, item, spider):
        # 写sql语句 插数据，没有表的话要先在数据库创建
        sql = self.get_sql(item)
        if not self.redis.redis_exists(sql):
            # 创建游标对象
            self.cursor = self.conn.cursor()
            # 提交事务
            try:
                self.cursor.execute(sql)
                last_id = int(self.conn.insert_id())  # 取最近插入的一条
                self.conn.commit()
                self.redis.save_redis(sql, last_id)
                # int(cursor.lastrowid)  # 最后插入行的主键ID
                # int(conn.insert_id())  # 最新插入行的主键ID，conn.insert_id()一定要在conn.commit()之前，否则会返回0
            except Exception as e:
                print(e)
                print('异常回滚')
                self.conn.rollback()
            return item
        else:
            print('已有相同数据无需插入')

    # 结束爬虫时调用
    def close_spider(self, spider):
        print('爬虫结束, 关闭通道')
        self.cursor.close()
        self.conn.close()
