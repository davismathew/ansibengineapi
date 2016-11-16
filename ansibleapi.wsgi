#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/home/davis/Documents/ansibleapi/")

from ansibleapi import app as application
#application.secret_key = 'Add your secret key'
