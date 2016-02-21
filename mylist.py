#!/usr/bin/python

import sys 
from pymongo import MongoClient
import ListAccessObject
import cgi, cgitb



connection = MongoClient()
db = connection.lists
lists = ListAccessObject.ListAccessObject(db)

form = cgi.FieldStorage()

list_name = form.getvalue('list_name')
item_to_add = form.getvalue('item_to_add')


lists.insert_item(list_name, item_to_add)

#print("Location: http://localhost/")

print "Content-type:text/html\r\n\r\n"
print "<html>"
print "Inserted!"
print list_name
print item_to_add
print "</html>"

print # to end the CGI response headers.

#render_template('combined.py')
