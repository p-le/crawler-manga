# -*- coding: utf-8 -*-
import scrapy
from mangacrawler.items import MangaItem

class MangakSpider(scrapy.Spider):
    name = "mangak"
    allowed_domains = ["mangak.info"]
    start_urls = ['http://mangak.info/ajin/']

    def parse(self, response):
        eles = response.xpath('//div[@class="chapter-list"]/div[@class="row"]')

        for ele in eles:
            chapter = ele.xpath('span/a/text()').extract_first()
            chapterUrl = ele.xpath('span/a/@href').extract_first()
            date = ele.xpath('span[2]/text()').extract_first()
            request = scrapy.Request(chapterUrl, callback=self.parse_chapter)
            request.meta['manga'] = "Ajin"
            request.meta['title'] = chapter
            request.meta['date'] = date
            yield request
        
    def parse_chapter(self, response):
        imgs = response.xpath('//div[@class="vung_doc"]/img/@src').extract()
        item = MangaItem()
        item['manga'] = response.meta['manga']
        item['title'] = response.meta['title']
        item['imgs'] = imgs
        item['date'] = response.meta['date']
        yield item
            
