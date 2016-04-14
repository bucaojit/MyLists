'''
Created on Mar 20, 2016

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
 

from flask import Flask, session, redirect, url_for, escape, request, render_template, jsonify, make_response, Markup
from cache_access import CacheAccess
from cache import CacheEngine
from optparse import Values
#
#  Contains flask operations
#
class CacheServer:
    '''
    classdocs
    '''
    title_length = 80
    desc_length = 300
    
    def __init__(self, config, app):
        '''
        Constructor
        '''
        self.config = config 
        if config['trace'] == "True": print 'TRACE: before CacheAccess'
        self.cache_access = CacheAccess(config)               
        if config['trace'] == "True": print 'TRACE: after CacheAccess'
        self.app = app
        if config['trace'] == "True": print 'TRACE: after self.app=app'
        self.cache = CacheEngine()
        
    def add_routes(self):
        if self.config['trace'] == "True": print 'TRACE: add_routes ENTER' 
        @self.app.route('/entry', methods=['POST','GET'])
        def form_entry():
            if self.config['trace'] == "True": print 'TRACE: form_entry ENTER' 
            error = None
            if request.method == 'POST':
                # request.form['item'] pass to the database
                summary = request.form['Title']
                description = request.form['Description']
                usefulness = request.form['usefulness']
                link_input = request.form['link_input']
                subcategory_text = request.form['subcategory_text']
                #subcategory_dropdown = request.form['subcategory_dropdown']
                category_text = request.form['category_text']
                #category_dropdown = request.form['category_dropdown']
                # Input validation
                #if subcategory_dropdown == 'select':
                #    return "need to set subcat"
                # Insert data into database
              
                # re-render, pass in error variable
                input_dict = {'summary':summary,
                              'description':description, 
                              'usefulness':usefulness,
                              'link_input':link_input,
                              'subcategory_text':subcategory_text,
                              #'subcategory_dropdown':subcategory_dropdown,
                              'category_text':category_text}
                            #'category_dropdown':category_dropdown}
                self.cache_access.entry_insert(input_dict)
                return render_template('inputform.html', error=error)
            if self.config['trace'] == "True": print 'TRACE: form_entry EXIT' 
            return render_template('inputform.html', error=error)

        @self.app.route('/view', methods=['POST','GET'])
        def view_single():
                str_id = request.args.get('str_id')
                row = self.cache_access.id_get(str_id)
                description = Markup(self.cache.n_to_br(row['description']))
                return render_template('singleview.html', entry=row, description=description)

        @self.app.route('/search', methods=['POST','GET'])
        def search():

            
            if request.method == 'POST':
                search_text = request.form.get('Search', None)
                category = request.form.get('category', None)
                subcategory = request.form.get('subcategory', None)
                if category == 'select':
                    category = None
                if subcategory == 'select':
                    subcategory = None
                if search_text == '':
                    search_text = None
                
                values = self.cache_access.search(search_text, category, subcategory)

                return render_template('simpleoutput.html', entries=self.process_values(values))
            categories = self.cache_access.distinct("category_text")
            subcategories = self.cache_access.distinct("subcategory_text")
            #categories = self.cache_access.get_all()
            #categories_set = set()
            #print str(categories)
            #    categories_set.add(cat['category_text'])
                
            #subcategories = self.cache_access.get_attribute('subcategory_text')
            entries = self.cache_access.newest_n(5, True)
            count = entries.count() -1
            #reversed_vals = [None]*count +1
            #for entry in entries:
            #    reversed_vals[count] = entry
            #    count -= 1
         
            return render_template('search.html', categories=categories, 
                                   subcategories=subcategories,
                                   entries=self.process_values(entries))
        
        @self.app.route('/viewcache', methods=['POST','GET'])
        def view():
            if request.method == 'POST':
                hiddenValue = request.form.get('to_view', None)
                
                if hiddenValue is not None:
                    # print '+' + hiddenValue + '+'
                    pdf_binary = self.cache_access.binary_get(hiddenValue)
                   
#                     handle = open('file123.txt','wb')
#                     # issue is it's none
#                     handle.write(pdf_binary)
#                     return "done"
                    response = make_response(pdf_binary.read())
                    response.headers['Content-Type'] = 'application/pdf'
                    response.headers['Content-Disposition'] = \
                        'inline; filename=%s.pdf' % hiddenValue
                    return response
            # values is dict
            values = self.cache_access.get_all()
            
#             outputstring="<html><body>"
#             for value in values:
#                 outputstring += str(value) + '<br />'
#             outputstring += '</body></html>'
            return render_template('simpleoutput.html', entries=values)
        
    def process_values(self, values):
        
        insert_values = []
        for value in values:
                # String truncating
                summary_str = value['summary']
                value['summary'] = (summary_str[:self.title_length] + '...') if len(summary_str) > self.title_length else summary_str
                desc_str = value['description']
                value['description'] = (desc_str[:self.desc_length] + '...') if len(desc_str) > self.desc_length else desc_str
                # Including the _id value needed for individual view
                value['str_id'] = str(value['_id'])
                insert_values.append(value)
        return insert_values
