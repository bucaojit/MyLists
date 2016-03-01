#!/usr/bin/python
import sys, os
sys.path.insert (0,'/var/www/flaskTest')
os.chdir("/var/www/flaskTest")
from flaskTest import app as application
