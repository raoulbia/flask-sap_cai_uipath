activate_this = '/home/ubuntu/cai_uipath/myenv/bin/activate_this.py'
with open(activate_this) as f:
        exec(f.read(), dict(__file__=activate_this))

import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/html/cai_uipath/")

from cai_uipath.app import app as application
