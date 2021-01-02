# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class OnlineShopItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    review_score = scrapy.Field()
    review_count = scrapy.Field()
    url = scrapy.Field()

