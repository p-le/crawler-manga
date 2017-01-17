# -*- coding: utf-8 -*-
import scrapy
from mangacrawler.items import MangaItem

class MangakSpider(scrapy.Spider):
    name = "mangak"
    allowed_domains = ["mangak.info"]
    start_urls = ['http://mangak.info/attack-on-titan-2r/']

    def parse(self, response):
        eles = response.xpath('//div[@class="chapter-list"]/div[@class="row"]')
        infoDiv = response.xpath('//div[@class="truyen_if_wrap"]')
        
        lis = infoDiv.xpath('ul/li')
        title = "Attack on Titan"
        genres = lis[2].xpath('a/text()').extract()
        view = int(lis[6].xpath('text()').extract_first().replace(',', ''))
        thumb = infoDiv.xpath('div/span/img/@src').extract_first()
        onGoing = False
        if  lis[4].xpath('text()').extract_first() == " Đang cập nhật":
            onGoing = True
        description = ''.join(response.xpath('//div[@class="truyen_description"]/div/p//text()').extract())

        for ele in eles:
            chapter = ele.xpath('span/a/text()').extract_first()
            chapterUrl = ele.xpath('span/a/@href').extract_first()
            date = ele.xpath('span[2]/text()').extract_first()
            request = scrapy.Request(chapterUrl, callback=self.parse_chapter)
            request.meta['manga'] = "Attack on Titan"
            request.meta['name'] = title.lower().replace(' ', '-')
            request.meta['description'] = description
            request.meta['thumb'] = thumb
            request.meta['genres'] = genres
            request.meta['view'] = view
            request.meta['onGoing'] = onGoing
            request.meta['title'] = chapter
            request.meta['date'] = date
            yield request
        
    def parse_chapter(self, response):
        imgs = response.xpath('//div[@class="vung_doc"]/img/@src').extract()
        item = MangaItem()
        item['manga'] = response.meta['manga']
        item['name'] = response.meta['name']
        item['description'] = response.meta['description']
        item['thumb'] = response.meta['thumb']
        item['genres'] = response.meta['genres']
        item['view'] = response.meta['view']
        item['onGoing'] = response.meta['onGoing']
        item['title'] = response.meta['title']
        item['imgs'] = imgs
        item['date'] = response.meta['date']
        yield item
            
