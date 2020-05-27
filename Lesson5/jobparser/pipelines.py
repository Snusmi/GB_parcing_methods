# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from pymongo import MongoClient
import hashlib
import re


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancies_lesson5

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]

        item['salary_min'] = None
        item['salary_max'] = None
        item['salary_currency'] = None

        if spider.name == 'hhru':
            if len(item['salary']) == 7:
                item['salary_min'] = item['salary'][1].replace(u'\xa0', u'')
                item['salary_max'] = item['salary'][3].replace(u'\xa0', u'')
                item['salary_currency'] = item['salary'][-2]
            elif len(item['salary']) == 5:
                item['salary_currency'] = item['salary'][-2]
                if 'от' in item['salary']:
                    item['salary_min'] = item['salary'][1].replace(u'\xa0', u'')
                elif 'до' in item['salary']:
                    item['salary_max'] = item['salary'][1].replace(u'\xa0', u'')

        if spider.name == 'sjru':
            if len(item['salary']) == 4:
                item['salary_currency'] = item['salary'][-1]
                item['salary_min'] = item['salary'][0].replace(u'\xa0', u'')
                item['salary_max'] = item['salary'][1].replace(u'\xa0', u'')

            elif len(item['salary']) == 3:
                item['salary'][2] = item['salary'][2].replace(u'\xa0', u'')
                item['salary_currency'] = re.findall('[a-zA-Zа-яА-Я]+', item['salary'][2])

                if 'от' in item['salary']:
                    item['salary_min'] = re.findall('\d+', item['salary'][2])
                elif 'до' in item['salary']:
                    item['salary_max'] = re.findall('\d+', item['salary'][2])

        if item['salary_min']:
            item['salary_min'] = int(item['salary_min'])

        if item['salary_max']:
            item['salary_max'] = int(item['salary_max'])

        item['_id'] = hashlib.sha1(item['link'].split('?')[0].encode()).hexdigest()
        item['company_name'] = ''.join(item['company_name']).replace(u'\xa0', u' ')
        item['company_address'] = ''.join(item['company_address'])
        item['site'] = spider.name
        del item['salary']

        collection.update_one({"_id": item['_id']}, {'$set': item}, upsert=True)
        return item

# class ItemsPipeline:
#
#     def inspect_items(self, item, spider):
#
#         if len(item['salary']) == 7:
#             item['salary_min'] = item['salary'][1].replace(u'\xa0', u'')
#             item['salary_max'] = item['salary'][3].replace(u'\xa0', u'')
#             item['salary_currency'] = item['salary'][-2]
#         elif len(item['salary']) == 5:
#             item['salary_currency'] = item['salary'][-2]
#             if 'от' in item['salary']:
#                 item['salary_min'] = item['salary'][1].replace(u'\xa0', u'')
#             elif 'до' in item['salary']:
#                 item['salary_max'] = item['salary'][1].replace(u'\xa0', u'')
#
#         item['_id'] = hashlib.sha1(item['link'].split('?')[0].encode()).hexdigest()
#         item['company_name'] = ''.join(item['company_name']).replace(u'\xa0', u' ')
#         item['company_address'] = ''.join(item['company_address'])
#         item['site'] = spider.name
#         del item['salary']
#         return item