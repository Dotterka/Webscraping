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
    color = scrapy.Field()
    display_type = scrapy.Field()
    display_size = scrapy.Field()
    display_resolution = scrapy.Field()
    chipset = scrapy.Field()
    chipset_model = scrapy.Field()
    internal_memory = scrapy.Field()
    ram = scrapy.Field()
    main_camera = scrapy.Field()
    selfie_camera = scrapy.Field()
    os = scrapy.Field()
    os_version = scrapy.Field()
    nfc_indicator = scrapy.Field()
    battery_type = scrapy.Field()
    battery_capacity = scrapy.Field()
