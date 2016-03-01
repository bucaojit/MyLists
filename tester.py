'''
Created on Feb 27, 2016

@author: hduser
'''
#!/usr/bin/python

from flask import Flask, session, redirect, url_for, escape, request
from pymongo import MongoClient
import ListAccessObject

connection = MongoClient()
db = connection.lists
lists = ListAccessObject.ListAccessObject(db)
item = 'item'
value = 'something'
hiddenValue = {item:value}
lists.delete_item(value)

if __name__ == '__main__':
    pass