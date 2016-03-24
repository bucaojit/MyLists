#!/usr/bin/python

#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import string 
class ListAccessObject(object):

        def __init__(self, database, name_input):
                self.db = database
                self.name = name_input
                self.mydb = database[name_input]

        def find_items(self):
                l = []
                for each_item in self.mydb.find():
                        l.append({'item':each_item['item'], \
                                  'list':each_item['list'], \
                                  'timestamp':each_item['_id'].generation_time})
                return l

        def last_items(self, value):
                l = []
                for each_item in self.mydb.find().sort('_id',-1).limit(value):
                #for each_item in self.mydb.find().limit(value):
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
