from marklogic_connector import MarkLogicConnector
from mongo_connector import MongoConnector
from cache import CacheEngine

class CacheAccess(object):
    database_name = 'cache'
    collection_name = 'entries'
    db_connection = ()
    cache = CacheEngine()
    
    def __init__(self, configuration):
        if configuration['database'] == 'mdb':
            self.db_connection = MongoConnector(configuration['address'],
                                                self.database_name, 
                                                self.collection_name)
        elif configuration['database'] == 'ml':
            self.db_connection = MarkLogicConnector(configuration['address'],
                                                    self.database_name,
                                                    self.collection_name)          
        '''
        '''
    def entry_insert(self, dict_entry):
        #pdf = self.cache.process_pdf(dict_entry['link_input'])
        #if pdf is not None:
        #    self.binary_insert(dict_entry['link_input'], pdf)
        #processed_entry = self.cache.process_html(dict_entry['link_input'])
        #    dict_entry['html'] = processed_entry
        self.db_connection.insert(dict_entry)
    
    def binary_insert(self, filename, binary_file):
        self.db_connection.insert_binary(filename, binary_file)
    
    def binary_get(self, filename):
        return self.db_connection.get_binary(filename)
        
    def get_all(self):
        return self.db_connection.get_all()
    
    def get_attribute(self, attribute):
        return self.db_connection.get_attribute(attribute)
    
    def distinct(self, attribute):
        return self.db_connection.distinct(attribute)
    
    def id_get(self, str_id):
        return self.db_connection.id_get(str_id)
    
    def search(self, search_text, category, subcategory):
        return self.db_connection.search(search_text, category, subcategory)
        
    def newest_n(self, n, reverse):
        return self.db_connection.newest_n(n, reverse)
    
