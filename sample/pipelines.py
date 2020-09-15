# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import pymongo
import sqlite3

"""                                                                                 MONGO DB
class MongodbPipeline(object):
    collection_name = "best_movies"

    def open_spider(self, spider):
        self.client = pymongo.MongoClient("mongodb+srv://ahmed:testtest@cluster0-pbhxl.mongodb.net/test?retryWrites=true&w=majority")
        self.db = self.client["IMDB"]

    def close_spider(self, spider):
        self.client.close()


    def process_item(self, item, spider):
        self.db[self.collection_name].insert(item)
        return item

"""        
#                                                                                   SQLlite3
class SQLlitePipeline(object):

    def open_spider(self, spider):
        self.connection = sqlite3.connect("sample.db")
        self.c = self.connection.cursor()
        try:
            self.c.execute('''
                CREATE TABLE example (
                    name TEXT,
                    link TEXT,
                    image_links TEXT
                )
            
            ''')
            self.connection.commit()
        except sqlite3.OperationalError:
            pass


    def close_spider(self, spider):
        self.connection.close()


    def process_item(self, item, spider):
        self.c.execute('''
            INSERT INTO example (name,link,image_links) VALUES(?,?,?)

        ''', (
            item.get('name'),
            item.get('link'),
            item.get('image_links')
        ))
        self.connection.commit()
        return item


