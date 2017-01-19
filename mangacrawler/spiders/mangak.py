# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlparse
from pathlib import Path
import re
from mangacrawler.items import MangaItem

class MangakSpider(scrapy.Spider):
    name = "mangak"
    allowed_domains = ["mangak.info"]
    start_urls = ['http://mangak.info/']

    def parse(self, response):
        mangaAs= response.xpath('//div[@class="update_item"]//a[contains(@class,"tooltip")]')
        for mangaA in mangaAs:
            manga = mangaA.xpath('text()').extract_first()
            mangaUrl = mangaA.xpath('@href').extract_first()
            request = scrapy.Request(mangaUrl, callback=self.parse_manga)
            request.meta['manga'] = manga
            yield request
    def parse_manga(self, response):
        eles = response.xpath('//div[@class="chapter-list"]/div[@class="row"]')
        infoDiv = response.xpath('//div[@class="truyen_if_wrap"]')
        
        lis = infoDiv.xpath('ul/li')
        o = urlparse(response.url)
        name = o.path.replace('/', '')

        genres = lis[2].xpath('a/text()').extract()
        view = int(lis[6].xpath('text()').extract_first().replace(',', ''))
        thumb = infoDiv.xpath('div/span/img/@src').extract_first()
        onGoing = False
        if  lis[4].xpath('text()').extract_first().lstrip().rstrip() == "Đang cập nhật":
            onGoing = True
        description = ''.join(response.xpath('//div[@class="truyen_description"]/div/p//text()').extract())

        for ele in eles:
            chapter = ele.xpath('span/a/text()').extract_first()
            chapterUrl = ele.xpath('span/a/@href').extract_first()
            date = ele.xpath('span[2]/text()').extract_first()
            request = scrapy.Request(chapterUrl, callback=self.parse_chapter)
            request.meta['name'] = name
            request.meta['manga'] = response.meta['manga']
            request.meta['description'] = description
            request.meta['thumb'] = thumb
            request.meta['genres'] = genres
            request.meta['view'] = view
            request.meta['onGoing'] = onGoing
            request.meta['title'] = chapter
            request.meta['date'] = date


            p = Path("crawled_urls")
            found = False
            if p.is_file():
                with p.open() as file:
                    for line in file:
                        if chapterUrl in line:
                            found = True
                    file.close()
            if not found:
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
        item['chapterName'] = response.meta['title'][response.meta['title'].index('chap'):].lower().replace(' ', '-').replace('-r', '')
        item['imgs'] = imgs
        item['url'] = response.url;
        item['date'] = response.meta['date']

        file = open("crawled_urls", "a")
        file.write(response.url + "\n")
        file.close()

        yield item