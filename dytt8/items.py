# -*- coding: utf-8 -*-
import scrapy


class Dytt8Item(scrapy.Item):
    title = scrapy.Field()
    publish_time = scrapy.Field()
    images = scrapy.Field()
    download_links = scrapy.Field()
    contents = scrapy.Field()