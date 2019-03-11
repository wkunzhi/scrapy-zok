# -*- coding: utf-8 -*-
# __author__ = "zok" 
# Date: 2019/3/7  Python: 3.7
import random
from scrapy import signals

from fake_useragent import UserAgent


class RandomUserAgentMiddleware(object):

    def __init__(self):
        self.agent = UserAgent()

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', self.agent.random)
