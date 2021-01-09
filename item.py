# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ElderScrollsItem(scrapy.Item):
    # define the fields for your item here like:
    allData= scrapy.Field()
    
    name = scrapy.Field()
    tradeId = scrapy.Field()
    itemId = scrapy.Field()
    quality = scrapy.Field()
    trader = scrapy.Field()
    location = scrapy.Field()
    price = scrapy.Field()
    quantity=scrapy.Field()
    lastSeen = scrapy.Field()
