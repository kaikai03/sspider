# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RobotItem(scrapy.Item):
    # define the fields for your item here like:
    tid = scrapy.Field()
    poster = scrapy.Field()
    title = scrapy.Field()
    post_time = scrapy.Field()
    reply = scrapy.Field()
    date = scrapy.Field()
    # last_updated = scrapy.Field(serializer=str)
