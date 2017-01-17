# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import logging
import pymongo
import bson

class MongoDBPipeLine(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB', 'data')
        )

    def open_spider(self, spider):
        try:
            self.client = pymongo.MongoClient(self.mongo_uri)
            self.client.server_info()
            self.db = self.client[self.mongo_db]
            logging.log(logging.DEBUG, "Mongo Connected")
        except pymongo.errors.ServerSelectionTimeoutError as err:
            logging.log(logging.DEBUG, err)

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        manga = self.db["manga"].find_one({"title": item['manga'] }, {"title": 1, "chapters.title": 1} )
        
        if not manga:
            _id = self.db["manga"].insert({
                "title": item['manga'],
                "name": item['name'],
                "description": item['description'],
                "thumb": item['thumb'],
                "genres": item['genres'],
                "view": item['view'],
                "onGoing": item['onGoing']
            })
        else:
            _id = manga["_id"]

        self.db["chapter"].update({"title": item['title']}, {
            "mangaId": _id,
            "title": item['title'],
            "created": item['date'],
            "imgs": item['imgs']
        }, upsert=True)