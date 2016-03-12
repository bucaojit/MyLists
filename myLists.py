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

# Author: Oliver
# https://github.com/bucaojit/MyLists

from flask import Flask, session, redirect, url_for, escape, request, render_template, jsonify
from pymongo import MongoClient
import pymongo
import lib.ListAccessObject as ListAccessObject
from requests.sessions import Session
from operator import itemgetter, attrgetter, methodcaller
from pytz import timezone
from datetime import datetime
from flask_restful import Resource, Api
import sys
import json

app = Flask(__name__)
api = Api(app)
connection = MongoClient("localhost", serverSelectionTimeoutMS=5000)
try:
    connection.server_info() 
except pymongo.errors.ServerSelectionTimeoutError as err:
    print "Unable to connect to MongoDB, exiting"
    print(err)
    sys.exit(1)

db = connection.lists
lists = ListAccessObject.ListAccessObject(db,'myitems')
archive = ListAccessObject.ListAccessObject(db,'archive')

def hello_world2(input):
    return 'Hello Warriors! And %s' % input

def getList(item):
    return str(item['list']).lower()

@app.route('/mycache', methods=['GET', 'POST'])
def mycache():
   # Idea here is to have a type of memcache, instead for
   # useful websites visited, ideas, images
   # This will have a text search that is searchable on
   # summary and description.  
   # Ideas for fields include
   #   1) Summary
   #   2) Description
   #   3) Category
   #   4) Link
   return "This is your cache"

class HelloWorld(Resource):
    def get(self):
        data= [{
           'first_name': 'Bob',
           'second_name': 'Smith',
           'titles': ['Mr', 'Developer']
        },
        {'list':'firstList'},
        {'list':'secondList'},
        {'item':'firstItem'}]

        data_jsond = json.dumps(data)
        value = json.dumps([1, 2, 3, "a", "b", "c"])
        to_jsonify = [{'first':'firstItem','list':'listval'}]
        return jsonify(results=data)

class SecondEndpoint(Resource):
    def get(self):
        return {'testEnd':'Point'}

api.add_resource(HelloWorld,'/')
api.add_resource(SecondEndpoint,'/endpoint')

@app.route('/checklist', methods=['GET', 'POST'])
def add_item():
    formHtml = '''
        <form action="" method="post">
            <table border="0">
            <tr>
                <td>
                    List: 
                </td>
                <td>
                    <input type=text name=list>
                </td>
            </tr>
            <tr>
                <td>
                    Item: 
                </td>
                <td>
                    <input type=text name=item>
                </td>
            </tr>
            <tr>
            <td></td>
                <td><input type=submit value=Submit></td>
            </tr>
            </table>
        </form>
    '''
    cssHtml = '''
        <html>
        <head>
        <title>MyLists</title>
        <style>
        table {
            width:100%;
        }
        table, th, td {
            border: 1px solid black;
            border-collapse: collapse;
        }
        th, td {
            padding: 5px;
            text-align: left;
        }
        table#t01 tr:nth-child(even) {
            background-color: #eee;
        }
        table#t01 tr:nth-child(odd) {
           background-color:#fff;
        }
        table#t01 th    {
            background-color: black;
            color: white;
        }
        </style>
        </head>
        <body>
    '''

    
    if request.method == 'POST':
        variable = request.form.get('list',None)
        variable2 = request.form.get('item',None)
        hiddenValue = request.form.get('to_delete',None)
        if hiddenValue is None:
            lists.insert_item(variable, variable2)
            #print "hello"
            
        else:
            lists.delete_item(hiddenValue)
            lists.delete_item(None)
            #print "nothing here"
        output = cssHtml + \
                     formHtml + \
                     '<table id="t01">' + \
                     '<tr> <th> List Name </th> <th> Item </th> <th>Timestamp</th><th></th></tr>'
        tableValues = lists.find_items()
        tableValues = sorted(tableValues, key=getList)
        
        for item in tableValues:
            output += '<tr><td>'
            output += str(item['list'])
            output += '</td><td>'
            output += '<a href="'
            output += str(item['item'])
            output += '">'
            output += str(item['item'])
            output += '</a>'
            output += '</td>'
            output += '<td>'
            #output += str(item['timestamp'])
            output += str(item['timestamp'].astimezone(timezone('US/Pacific')).strftime("%m-%d-%Y %I:%M%p"))
            output += '</td>'

            output += '<td>'
            output += '<form action="" method="post">'
            output += '<input type=hidden value="'
            output += str(item['item'])
            output += '" name="to_delete"></input>'
            output += '<input type=submit value=Delete>'
            output += '<input type=submit value=Archive>'
            output += '</form></td></tr>'
        output += '</body>'
        output += '</table>'
        output += '</html>'
        
    
        return output
    tableValues = lists.find_items()
    tableValues = sorted(tableValues, key=getList)

    output = cssHtml + \
             formHtml + \
             '<table id="t01">' + \
             '<tr> <th> List Name </th> <th> Item </th> <th>Timestamp</th><th></th></tr>'
    for item in tableValues:
        output += '<tr><td>'
        output += str(item['list'])
        output += '</td><td>'
        output += '<a href="'
        output += str(item['item'])
        output += '">'
        output += str(item['item'])
        output += '</a>'
        output += '</td>'
        output += '<td>'
        #output += str(item['timestamp'])
        output += str(item['timestamp'].astimezone(timezone('US/Pacific')).strftime("%m-%d-%Y %I:%M%p"))
        output += '</td>'
        output += '<td>'
        output += '<form id = "form1" action="" method="post">'
        output += '<input type=hidden value="'
        #output += 'OliverValue'
        output += str(item['item'])
        output += '" name="to_delete"></input>'
        output += '<input type=submit name="delete" value="Delete" />'
        output += '<input type=submit name="archive" value="Archive" /></form>'
        output += '</td></tr>'
    output += '</body>'
    output += '</table>'
    output += '</html>'
    return output

#@app.route('/')
#def index():
#    return 'this is the index'

@app.route('/moreo')
def hello_world4():
    return 'more4'

@app.route('/lists')
def mylist():
    toOutput = lists.find_items()
    valueToOutput = "Hello Lists <br /><br />"
    for value in toOutput:
        valueToOutput += str(value['item'])
        valueToOutput += '<br />'
    return valueToOutput

@app.route('/more')
def hello_world3():
    return '''
<html>
   <head>
   Hello
   </head>
   <br />
   <body>
   World
   </body>
</html>
'''

@app.route('/template')
def templateTest():
   error=None
   return render_template('login.html', error=error)

@app.route('/index')
def hello_world():
    return 'Hello Warriors! And %s' % input

if __name__ == '__main__':
    #app.secret_key = 'super secret key'
    #app.config['SESSION_TYPE'] = 'filesystem'

    #session.init_app(app)
    app.run(debug=True)
