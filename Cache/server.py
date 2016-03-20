#!/usr/bin/python

from flask import Flask, session, redirect, url_for, escape, request, render_template, jsonify

app = Flask(__name__)

@app.route('/template')
def show_template():
    #return app.root_path
    return render_template('inputform.html')

if __name__ == '__main__':
    app.run(debug=True)
