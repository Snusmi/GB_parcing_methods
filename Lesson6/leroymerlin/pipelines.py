# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
from pathlib import Path
import os
import hashlib
import re

class LeroymerlinItemCleaner(object):

    def process_item(self, item, spider):

        item['folder_name'] = item['link'].split('/')[-2].replace('-', '_')

        if item['price']:
            item['price'] = float(''.join(item['price'].split(' ')))

        return item

class LeroymerlinPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.leroymerlin

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item


class LeroymerlinPhotoPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        if item['photo']:
            for img in item['photo']:
                try:
                    yield scrapy.Request(img, meta={'item': item})
                except Exception as e:
                    print(e)

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        folder_name = item['folder_name']
        url = request.url
        media_guid = hashlib.sha1(to_bytes(url)).hexdigest()
        media_ext = os.path.splitext(url)[1]
        return f'full/{folder_name}/%s%s' % (media_guid, media_ext)

    def item_completed(self, results, item, info):
        if results:
            item['photo'] = [itm[1] for itm in results if itm[0]]
        return item

