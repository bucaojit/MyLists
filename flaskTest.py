#!/usr/bin/python
from flask import Flask, session, redirect, url_for, escape, request
from pymongo import MongoClient
import ListAccessObject
from requests.sessions import Session
from operator import itemgetter, attrgetter, methodcaller

app = Flask(__name__)
connection = MongoClient()
db = connection.lists
lists = ListAccessObject.ListAccessObject(db)

@app.route('/mytest/<input>')
def hello_world2(input):
    return 'Hello Warriors! And %s' % input

def getList(item):
    return str(item['list']).lower()

@app.route('/additem', methods=['GET', 'POST'])
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
                <td><input type=submit value=Submit></td>
            </tr>
            </table>
        </form>
    '''
    cssHtml = '''
        <html>
        <head>
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
            output += str(item['timestamp'])
            output += '</td>'

            output += '<td>'
            output += '<form action="" method="post">'
            output += '<input type=hidden value="'
            output += str(item['item'])
            output += '" name="to_delete"></input>'
            output += '<input type=submit value=Delete></form></td></tr>'
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
        output += str(item['timestamp'])
        output += '</td>'
        output += '<td>'
        output += '<form id = "form1" action="" method="post">'
        output += '<input type=hidden value="'
        #output += 'OliverValue'
        output += str(item['item'])
        output += '" name="to_delete"></input>'
        output += '<input type=submit value=Delete></form>'
        output += '</td></tr>'
    output += '</body>'
    output += '</table>'
    output += '</html>'
    return output

@app.route('/')
def index():
    return 'this is the index'

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

@app.route('/index')
def hello_world():
    return 'Hello Warriors! And %s' % input

if __name__ == '__main__':
    #app.secret_key = 'super secret key'
    #app.config['SESSION_TYPE'] = 'filesystem'

    #session.init_app(app)
    app.run(debug=True)
