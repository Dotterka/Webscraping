# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random


class RandomUserAgentMiddleware(object):
    def __init__(self):
        self.agents = self.read_user()

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', random.choice(self.agents))

    def read_user(self):
        with open("useragents.txt", "r") as f:
            agents = f.read().splitlines()
            return agents
