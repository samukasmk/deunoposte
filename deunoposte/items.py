# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class GameResultItem(scrapy.Item):
    date = scrapy.Field()
    datetime = scrapy.Field()
    game = scrapy.Field()
    state = scrapy.Field()
    position = scrapy.Field()
    result = scrapy.Field()
    ten = scrapy.Field()
    animal = scrapy.Field()



