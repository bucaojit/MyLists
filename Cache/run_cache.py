#!/usr/bin/python

from flask import Flask, session, redirect, url_for, escape, request, render_template, jsonify
import cache

app = Flask(__name__)



@app.route('/template')
def show_template():
    #return app.root_path
    return render_template('inputform.html')

def test_method():
    print "running test method"
    
    @app.route('/testmethod')
    def testhandle():
        return "The method does work"

if __name__ == '__main__':
    test_method()
    
    #mycore.testrun()
    app.run(debug=True)

#
#  Ideas:  Make like a journal
#          Forcing login
#          Mongo for cache, Search = ElasticSearch
#          Structure, it's setup
#          Keep it as a simple setup for now