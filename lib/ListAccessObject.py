#!/usr/bin/python
import string 
class ListAccessObject(object):

        def __init__(self, database, name_input):
                self.db = database
                self.name = name_input
                self.mydb = database[name_input]

        def find_items(self):
                l = []
                for each_item in self.mydb.find():
                        print each_item
                        l.append({'item':each_item['item'], \
                                  'list':each_item['list'], \
                                  'timestamp':each_item['_id'].generation_time})
                return l

        def insert_item(self, list_name, newitem):
                newitem = {'list':list_name, 'item':newitem}
                self.mydb.insert(newitem)

        def delete_item(self, item):
                newitem = {'item':item}
                self.mydb.delete_many(newitem)