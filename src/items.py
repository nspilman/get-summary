# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PioneerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class MainebizItem(scrapy.Item):
    filename = scrapy.Field()
    text_content = scrapy.Field()