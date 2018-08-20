import os, sys, site

from raven.contrib.django.raven_compat.middleware.wsgi import Sentry
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SeguimientoUCSG.settings")
# os.environ["DJANGO_SETTINGS_MODULE"] = "SeguimientoUCSG.settings"

try:
    # Add the site packages, to override any system-wide packages
    site.addsitedir('/var/www/SeguimientoUCSG/venv/lib/python2.7/site-packages')
    
    # Activate the virtualenv
    activate_this = os.path.expanduser(os.path.abspath('/var/www/SeguimientoUCSG/venv/bin/activate_this.py'))
    execfile(activate_this, dict(__file__=activate_this))
except Exception as e:
    print e

application = get_wsgi_application()
