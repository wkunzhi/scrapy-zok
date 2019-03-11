# -*- coding: utf-8 -*-
# __author__ = "zok" 
# Date: 2019/3/7  Python: 3.7

import redis
import hashlib

from zok.zok_config import REDIS_PORT, REDIS_DB_NAME, REDIS_HOST, REDIS_USER, REDIS_PASSWORD


class CacheRedis(object):
    pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB_NAME, decode_responses=True)
    r = redis.Redis(connection_pool=pool)
    # 加上decode_responses=True，写入的键值对中的value为str类型，不加这个参数写入的则为字节类型。

    # 1. 根据储存数据取值判断是否存在
    # 2. 不存在 映射一个redis.set('数据', 数据_id)
    # 3. 不存在-已有数据: 需要更新
    # 4. 不存在-无数据: 需要插入
    # 5. 存在 直接跳过储存

    # BUG 在redis数据库丢失的情况下【会全体重新录入】

    @staticmethod
    def get_md5(data):
        md5 = hashlib.md5(data.encode('utf-8')).hexdigest()
        return md5

    def redis_exists(self, data):
        """
        验证hash是否存在， 有返回True，没有就储存
        :param data: 要储存的数据
        :param data_id: 对应的mysql id
        :return: True or False
        """
        md5 = self.get_md5(data)
        if self.r.exists(md5):
            return True
        else:
            return False

    def save_redis(self, sql, data_id):
        md5 = self.get_md5(sql)
        self.r.set(md5, data_id)

