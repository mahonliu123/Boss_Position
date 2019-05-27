# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class BossPipeline(object):
    def process_item(self, item, spider):
        location = item['location']
        if location:
            item['location'] = location.strip().replace(' ', '/')
        return item


class MongoPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        cls.mongo_uri = crawler.settings.get('MONGO_URI', 'localhost:27017')
        cls.mongo_db = crawler.settings.get('MONGO_DB', 'scrapy_Boss_Position_data')
        return cls()
        pass

    def process_item(self, item, spider):
        self.db['Position'].insert(dict(item))
        return item
        pass

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        pass

    def close_spider(self, spider):
        self.client.close()
