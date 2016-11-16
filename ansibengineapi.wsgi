import sys
import logging
#import mod_wsgi
#print mod_wsgi.version
#PROJECT_DIR = '/var/www/html/ansibengineapi/'
#if PROJECT_DIR not in sys.path:
#    sys.path.insert(0, PROJECT_DIR)
#def execfile(filename):
#    globals = dict( __file__ = filename )
#    exec( open(filename).read(), globals )

#activate_this = os.path.join( PROJECT_DIR,'flask/bin', 'activate_this.py')
#execfile( ativate_this )

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/html/ansibengineapi/")
#sys.stderr.write('\n'.join(sys.path))
#print mod_wsgi.version

from app import app as application
#application.secret_key = 'Add your secret key'
