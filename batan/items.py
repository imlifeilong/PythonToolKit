# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BatanItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    source = scrapy.Field()
    area = scrapy.Field()
    license = scrapy.Field()
    legal = scrapy.Field()
    province = scrapy.Field()
    add_date = scrapy.Field()


class ProjectItem(scrapy.Item):
    name = scrapy.Field()
    prjName = scrapy.Field()
    buildCorpName = scrapy.Field()
    prjType = scrapy.Field()
    id = scrapy.Field()
    add_date = scrapy.Field()
