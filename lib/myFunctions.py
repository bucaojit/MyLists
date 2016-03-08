#!/usr/bin/python
import re

m = re.search('http://', ' http://www.google.com')
m.group(0)

n = re.search('.\..', 'www.google.com')
n.group(0)

# re.search() vs re.match()

# Also, create as library and functions
