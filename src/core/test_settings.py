from .settings import *

# TEST_DOMAIN = 'navsys.local'

if ls.get('TEST_ALLOWED_HOSTS') is not None:
    ALLOWED_HOSTS = ls['TEST_ALLOWED_HOSTS']

if ls.get('TEST_DB_NAME') is not None:
    DATABASES['default'].setdefault('TEST', {})['NAME'] = ls['TEST_DB_NAME']

if ls.get('TEST_DB_USER') is not None:
    DATABASES['default']['USER'] = ls['TEST_DB_USER']

if ls.get('TEST_DB_PASS') is not None:
    DATABASES['default']['PASSWORD'] = ls['TEST_DB_PASS']

if ls.get('TEST_CACHE_REDIS_DB') is not None:
    REDIS_DATABASES['cache']['DB'] = ls['TEST_CACHE_REDIS_DB']

if ls.get('TEST_SESSION_REDIS_DB') is not None:
    REDIS_DATABASES['sessions']['DB'] = ls['TEST_SESSION_REDIS_DB']

if ls.get('TEST_CACHE_ENABLED') is not None:
    CACHE_ENABLED = ls['TEST_CACHE_ENABLED']

update_caches(CACHES, CACHE_ENABLED)

# TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

TMP_DIR = ROOT_DIR.child('var', 'tmp', 'test_tmp')
LOG_DIR = ROOT_DIR.child('var', 'tmp', 'test_log')
MEDIA_ROOT = ROOT_DIR.child('var', 'tmp', 'test_media')

# INSTALLED_APPS += ('django_nose',)

# del LOGGING['loggers']['django']
# LOGGING['loggers']['django']['handlers'].append('debug_log_file')
# LOGGING['loggers']['django']['level'] = 'DEBUG'
LOGGING['loggers'][''] = {
    'handlers': ['debug_log_file'],
    'level': 'DEBUG',
    'propagate': True,
}
