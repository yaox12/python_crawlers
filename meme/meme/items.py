# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MemeItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_caption = scrapy.Field()
    store_path = scrapy.Field()
    outfile = scrapy.Field()
