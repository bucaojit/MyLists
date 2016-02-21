#!/usr/bin/python
import string 
class ListAccessObject(object):

        def __init__(self, database):
                self.db = database
                self.myitems = database.myitems

        def find_items(self):
                l = []
                for each_item in self.myitems.find():
                        l.append({'item':each_item['item'], 'list':each_item['list']})
                return l

        def insert_item(self, list_name, newitem):
                newitem = {'list':list_name, 'item':newitem}
                self.myitems.insert(newitem)
