import os
import sys
from unipath import Path


sys.path.insert(0,  Path(__file__).absolute().ancestor(3))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
