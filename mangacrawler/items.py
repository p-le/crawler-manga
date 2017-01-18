# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class MangaItem(Item):
    manga = Field()
    name = Field()
    chapterName = Field()
    description = Field()
    thumb = Field()
    genres = Field()
    view = Field()
    onGoing = Field()
    title = Field()
    url = Field()
    imgs = Field()
    date = Field()