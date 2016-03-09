#!/usr/bin/python
import sys, os
sys.path.insert (0,'/var/www/MyLists')
os.chdir("/var/www/MyLists")
from myLists import app as application
