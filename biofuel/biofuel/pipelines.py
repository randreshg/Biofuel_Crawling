# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .items import BiofuelItem
from pymongo import MongoClient
import json
import os

class BiofuelPipeline:
    cluster = MongoClient("mongodb+srv://randreshg:INFOCRAWLING@cluster0.lyoos.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = cluster["crawling"]
    articles = db["articles"]
    content = db["content"]

    def open_spider(self, spider):
        self.file_articles = open('output/articles.json', 'w')
        self.file_content = open('output/content.json', 'w')
        # Initial content
        self.file_articles.write("[")
        self.file_content.write("[")

    def close_spider(self, spider):
        # Articles
        self.file_articles.seek(self.file_articles.tell() - 3, os.SEEK_SET)
        self.file_articles.write("]")
        self.file_articles.close()
        # Content
        self.file_content.seek(self.file_content.tell() - 3, os.SEEK_SET)
        self.file_content.write("]")
        self.file_content.close()


    def write_article(self, item):
        line = json.dumps(
            dict(item),
            indent = 4,
            sort_keys = False,
            separators = (',', ': ')
        ) + ", \n"
        self.file_articles.write(line)
        self.articles.insert_one(dict(item))

    def write_content(self, item):
        line = json.dumps(
            dict(item),
            indent = 4,
            sort_keys = False,
            separators = (',', ': ')
        ) + ", \n"
        self.file_content.write(line)
        self.content.insert_one(dict(item))

    def process_item(self, item, spider):
        if isinstance(item, BiofuelItem):
            self.write_article(item)
        else:
            self.write_content(item)
        return item
