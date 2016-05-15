#!/usr/bin/python

import sys
sys.path.append('/usr/local/lib/python2.7/dist-packages')
from flask import Flask, session, redirect, url_for, escape, request, render_template, jsonify
#from cache import cache
from server import CacheServer
#from mongo_connector import MongoConnector

app = Flask(__name__)
app.config.from_object('config')

# From configuration
# if config ==mongo:
#     conn = mongo_connector()
# elif config == MarkLogic:
#     conn = ml_connector()
# elf config == HBase:
#     conn = hbase_connector()
# conn = mongo_connector()

# This should 'get' from config file
database_type = 'mdb'
ip_addr = 'localhost'
tracing = "False"

config = {"database":database_type, "address":ip_addr, "trace":tracing}

myserv = CacheServer(config, app)
if config['trace'] == "True": print ('TRACE: after myserv = CacheServer')

if config['trace'] == "True": print ('TRACE: after add_routes()')
myserv.add_routes()

if __name__ == '__main__':
    app.run(debug=True)
    

