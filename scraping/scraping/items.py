# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ScrapingItem(scrapy.Item):
    filmID = scrapy.Field()
    filmTitle = scrapy.Field()
    user = scrapy.Field()
    rating = scrapy.Field()
    date = scrapy.Field()
    review = scrapy.Field()