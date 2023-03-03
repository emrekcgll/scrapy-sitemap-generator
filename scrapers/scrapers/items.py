# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SitemapItem(scrapy.Item):
    loc = scrapy.Field()
    priority = scrapy.Field()
    lastmod=scrapy.Field()
    changefreq=scrapy.Field()