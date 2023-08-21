#!/usr/bin/python
import sys
import logging
 
sys.path.insert(0, '/var/www/from-england-to-istanbul')
sys.path.insert(0, '/home/hanne/miniconda3/lib/python3.11/site-packages')
 
# Set up logging
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
 
# Import and run the Flask app
from main import app as application

application.secret_key = 'MySitesSecurityIsQuestionable'
