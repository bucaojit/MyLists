'''
@author: oliver
'''
 
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
 
from pymongo import MongoClient
from connector_interface import Connector
import gridfs
from bson.objectid import ObjectId

#
#  MongoDB Connection Interface
#
class MongoConnector(Connector):
    address=()
    server_timeout=5000
    
    def __init__(self, address, database_name, collection_name):
        self.database_name = database_name
        self.collection_name = collection_name
        self.address = address
        self.connect()

    def connect(self):
        self.connection = MongoClient(self.address, serverSelectionTimeoutMS=self.server_timeout)
        self.grid_fs = gridfs.GridFS(self.connection.pdf_database)
        self.db_connection = self.connection[self.database_name]
        self.db_collection = self.db_connection[self.collection_name]
        #self.cache_accessor = CacheAccess(self.db_connection, self.db_collection)
        
        return
    def disconnect(self):
        return
    def insert(self, values):
        return self.db_collection.insert(values)
    
    def insert_binary(self, filename, binary_file):
        mimetype = 'application/pdf'
        self.grid_fs.put(binary_file, contentType=mimetype, filename=filename)
    
    def get_binary(self, filename):
        return self.grid_fs.get_last_version(filename)
        
    def delete(self, values):
        return 
    
    def get_all(self):
        return self.db_collection.find()
    
    def get_attribute(self, attribute):
        return self.db_collection.find({},{attribute:1})

    def newest_n(self, n, reverse):
        if reverse:
            return self.db_collection.find().sort('$natural',-1).limit(5)
        else:
            return self.db_collection.find().skip(self.db_collection.count() - n)
    
    def distinct(self, attribute):
        return self.db_collection.distinct(attribute)
    
    def id_get(self, str_id):
        objid = ObjectId(str_id)
        return self.db_collection.find_one({'_id':objid})

    def delete_one(self, str_id):
        objid = ObjectId(str_id)
        self.db_collection.delete_one({'_id':objid})

    def entry_update(self, str_id, dict_entry):
        objid = ObjectId(str_id)
        return self.db_collection.replace_one({'_id':objid}, dict_entry)
    
    def search(self, search_text, category, subcategory):
        search_dict = {}
        #print 'category=' + category
        if category is not None:
            search_dict ["category_text"] = category
        if subcategory is not None:
            search_dict ["subcategory_text"] = subcategory
        if search_text is not None:
            search_entry = { '$search' : search_text }
            search_dict['$text'] = search_entry
        
        #search_string += ' \$text: { \$search: "' + search_text + '" }'
        # return self.db_collection.find({search_string})
        #return self.db_collection.find({ 'category_text': category,
        #                                 '$text' : { '$search': search_string} })
        return self.db_collection.find(search_dict,{'score': {'$meta': 'textScore'}}).sort([('score', {'$meta': 'textScore'})])
