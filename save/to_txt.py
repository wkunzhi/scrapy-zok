# -*- coding: utf-8 -*-
# __author__ = "zok" 
# Date: 2019/3/7  Python: 3.7
from zok.zok_config import TXT_NAME


class SaveToTxtBase(object):
    """
    存储txt文件基类
    """
    # 1. 链接数据库
    # 2. 执行sql语句
    # 3. 提交
    file = None

    # 爬虫开始执行
    def open_spider(self, spider):
        print('爬虫开始，开启txt写出通道')
        self.file = open(TXT_NAME, 'a', encoding='utf-8')

    def process_item(self, item, spider):
        try:
            res = dict(item)
            line = res['name']
            self.file.write(line + '\n')
        except:
            pass

    # 结束爬虫时调用
    def close_spider(self, spider):
        print('爬虫结束, 关闭文档写出通道')
        self.file.close()
