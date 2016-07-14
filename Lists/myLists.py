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

import sys
sys.path.append('/usr/local/lib/python2.7/dist-packages')
from flask import Flask, session, redirect, url_for, escape, request, render_template, jsonify, flash
from flask import Flask as flask
from flask.ext.login import LoginManager
import flask.ext.login as flask_login
from lib.forms import LoginForm
from flask.ext.login import login_user, logout_user, current_user, login_required
from pymongo import MongoClient
import pymongo
import lib.ListAccessObject as ListAccessObject
from requests.sessions import Session
from operator import itemgetter, attrgetter, methodcaller
from pytz import timezone
from datetime import datetime
from flask_restful import Resource, Api
import configparser
from lib.user import User
import json
from werkzeug.security import check_password_hash

configFile = 'config/lists.config'
ip_addr = 'localhost'

app = Flask(__name__)
app.config.from_object('config')
api = Api(app)
connection = MongoClient(ip_addr, serverSelectionTimeoutMS=5000)
Config = configparser.ConfigParser()
login_manager = LoginManager()
login_manager.init_app(app)

# Adding config file to specify options ie database type, ip-address, port
Config.read(configFile)


try:
    connection.server_info() 
except pymongo.errors.ServerSelectionTimeoutError as err:
    print ("Unable to connect to MongoDB, exiting")
    print(err)
    sys.exit(1)

db = connection.lists
list_names = ListAccessObject.ListAccessObject(db,'listnames')
lists = ListAccessObject.ListAccessObject(db,'myitems')
archive = ListAccessObject.ListAccessObject(db,'archive')
backlog = ListAccessObject.ListAccessObject(db,'backlog')
login = db['login']

@login_manager.user_loader
def load_user(username):
    u = app.config['USERS_COLLECTION'].find_one({"_id": username})
    if not u:
        return None
    return User(u['_id'])

def getList(item):
    return str(item['list']).lower()


class SecondEndpoint(Resource):
    def get(self):
        listValues = lists.find_items()
        sortedVals = sorted(listValues, key=getList)
        return jsonify(result=sortedVals)


class LastInsertedEndpoint(Resource):
    def get(self, count):
        listValues = lists.last_items(count)
        return jsonify(result = listValues)

api.add_resource(SecondEndpoint,'/endpoint')
api.add_resource(LastInsertedEndpoint,'/latest/<int:count>')

@app.route('/test', methods=['GET', 'POST'])
def template_test():
    tableValues = lists.find_items()
    tableValues = sorted(tableValues, key=getList)
    return render_template('lists.html', items=tableValues)

@app.route('/completed', methods=['GET', 'POST'])
@login_required
def view_completed():
    if request.method == 'POST':
        hiddenValue = request.form.get('to_delete',None)
        archive.delete_item(hiddenValue)
    buttons = [ 'X' ]
    tableValues = archive.find_items()
    tableValues = sorted(tableValues, key=getList)
    return render_template('lists.html', 
                           items=tableValues,
                           name='completed',
                           buttons=buttons)

@app.route('/backlog', methods=['GET', 'POST'])
@login_required
def view_backlog():

    if request.method == 'POST':
        hiddenValue = request.form.get('to_delete',None)
        hiddenList = request.form.get('list_name', None)
        if request.form.get('Completed', None) is not None:
            archive.insert_item(hiddenList, hiddenValue)
        elif request.form.get('Backlog', None) is not None:
            backlog.insert_item(hiddenList, hiddenValue)
        elif request.form.get('CheckList', None) is not None:
            lists.insert_item(hiddenList, hiddenValue)
        
        backlog.delete_item(hiddenValue)
    buttons = [ 'CheckList', 'Completed', 'X' ]
    tableValues = backlog.find_items()
    tableValues = sorted(tableValues, key=getList)
    return render_template('lists.html', 
                           items=tableValues, 
                           name='backlog', 
                           buttons=buttons)

@app.route('/namedlist', methods=['GET', 'POST'])
def namedlist():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if not 'name' in request.args:
        return 'Missing name option, please add ie ?name=<name>'
    listName  = request.args.get('name')
    namedlist = ListAccessObject.ListAccessObject(db, listName)
    if request.method == 'POST':
        variable = request.form.get('list',None)
        variable2 = request.form.get('item',None)
        hiddenValue = request.form.get('to_delete',None)
        hiddenList = request.form.get('list_name', None)
        if hiddenValue is None:
            namedlist.insert_item(variable, variable2)
            
        else:
            if request.form.get('Completed', None) is not None:
                archive.insert_item(hiddenList, hiddenValue)
            elif request.form.get('Backlog', None) is not None:
                backlog.insert_item(hiddenList, hiddenValue)
            namedlist.delete_item(hiddenValue)
            namedlist.delete_item(None)
        tableValues = namedlist.find_items()
        tableValues = sorted(tableValues, key=getList)
        tableValues = add_time(tableValues)
        
        return render_template('checklist.html', name=listName, session=session, items=tableValues)
    
    tableValues = namedlist.find_items()
    tableValues = sorted(tableValues, key=getList)
    
    tableValues = add_time(tableValues)

    return render_template('checklist.html', name=listName, session=session, items=tableValues)

@app.route('/checklist', methods=['GET', 'POST'])
def add_item():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if request.method == 'POST':
        variable = request.form.get('list',None)
        variable2 = request.form.get('item',None)
        hiddenValue = request.form.get('to_delete',None)
        hiddenList = request.form.get('list_name', None)
        if hiddenValue is None:
            lists.insert_item(variable, variable2)
            
        else:
            if request.form.get('Completed', None) is not None:
                archive.insert_item(hiddenList, hiddenValue)
            elif request.form.get('Backlog', None) is not None:
                backlog.insert_item(hiddenList, hiddenValue)
            lists.delete_item(hiddenValue)
            lists.delete_item(None)
        tableValues = lists.find_items()
        tableValues = sorted(tableValues, key=getList)
        tableValues = add_time(tableValues)
        
        return render_template('checklist.html', name='CheckList', session=session, items=tableValues)
    
    tableValues = lists.find_items()
    tableValues = sorted(tableValues, key=getList)
    
    tableValues = add_time(tableValues)

    return render_template('checklist.html', name='CheckList', session=session, items=tableValues)

@app.route('/addlist', methods=['GET', 'POST'])
def add_list():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if request.method == 'POST':
        variable = request.form.get('list',None)
        hiddenValue = request.form.get('to_delete',None)
        hiddenList = request.form.get('list_name', None)
        if hiddenValue is None:
            list_names.insert_listname(variable)
            
        else:
            # delete the list from the database
            list_names.delete_listname(hiddenList)
        tableValues = list_names.find_lists()
        tableValues = sorted(tableValues, key=getList)
        
        return render_template('addlist.html', session=session, items=tableValues)
    tableValues = list_names.find_lists()
    tableValues = sorted(tableValues, key=getList)

    return render_template('addlist.html', session=session, items=tableValues)

def add_time(list_input):
    list_output = []
    for entry in list_input:
        entry['datetime'] = str(entry['timestamp'].astimezone(timezone('US/Pacific')).strftime("%m-%d-%Y %I:%M%p"))
        list_output.append(entry)
    return list_output

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

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout the current user."""
    #user = current_user
    #user.authenticated = False
    #db.session.add(user)
    #db.session.commit()
    logout_user()
    return render_template("logout.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(csrf_enabled=False)
#    Work in progress
#    user_id = request.cookies.get('SessionProdTools')
#    if user_id:
#        user = 
    if request.method == 'POST' and form.validate_on_submit():
        user = app.config['USERS_COLLECTION'].find_one({"_id": form.username.data})
        #user = MongoClient()['blog'].users.find_one({"_id": form.username.data})

        if user and User.validate_login(user['password'], form.password.data):
            user_obj = User(user['_id'])
            login_user(user_obj, remember=True)
            flash("Logged in successfully!", category='success')
            return redirect(request.args.get("next") or url_for("add_item"))
        flash("Wrong username or password!", category='error')
    return render_template('login.html', title='login', form=form)


if __name__ == '__main__':
    #app.secret_key = 'super secret key'
    #app.config['SESSION_TYPE'] = 'filesystem'

    #session.init_app(app)
    app.run(debug=True)


@app.route('/additem', methods=['GET', 'POST'])
def add_form():
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
                     formHtml     
        return output

    output = cssHtml + \
             formHtml
    return output

