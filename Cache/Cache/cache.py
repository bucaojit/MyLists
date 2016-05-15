'''
Created on Mar 19, 2016

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
 
#import ConfigParser
#from mongo_connector import MongoConnector
import pdfkit
import urllib3
from bson.binary import Binary
from bs4 import BeautifulSoup
import re
import sys
#from lxml.html.builder import LINK

#
#  Contains computing type work not related to server or database
#
class CacheEngine(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        # Later on, choose from config file
        self.poolmanager = urllib3.PoolManager()

    def testrun(self):
        print ("This is test run")
        
    def process_pdf(self, link):
        if link != '':
            try:
            #print link
                pdf = pdfkit.from_url(str(link), False)
                return Binary(pdf)
                #print link
            except IOError as e:
                print ("Unexpected error:", sys.exc_info()[0])
                print (e.errno)
                print (e)
                return
        return
    
    def n_to_br(self, description):
        return description.replace('\n',' <br> ')
        #return description

    def space_convert(self, description):
        return description.replace(' ','&nbsp;')
    
    def process_html(self, link):

            
        # Make these complete in parallel
        response = self.poolmanager.urlopen('GET', link, True)
    
        if response.status == 200:
            #save response.data
            soup = BeautifulSoup(response.read(), 'html.parser')
            #text = soup.body.div.findall(text=True)
            text = soup.find_all(text=True)
            def visible(element):
                if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
                    return False
                elif re.match('<!--.*-->', (element).encode('utf-8')):
                    return False
                return True
    
            return  '|'.join(filter(visible, text))
            
            #cache_entry['html'] = unicode(''.join(visible_texts), "ISO-8859-1")
            #cache_entry['html'] = '|'.join(visible_texts)
        else:
            return "ERROR: Please retry HTML processing"

        
