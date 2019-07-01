import sys
import os
from unipath import Path
from .settings_base import BASE_DIR, ROOT_DIR, LOG_DIR, TMP_DIR, ls


DEBUG = ls.get('DEBUG', False)
CACHE_ENABLED = ls.get('CACHE_ENABLED', False)
INTERNAL_IPS = ls.get('INTERNAL_IPS', ['127.0.0.1'])

ADMINS = ls.get('ADMINS', [])
if not DEBUG and not len(ADMINS):
    raise AssertionError('ADMINS must be non empty')

ALLOWED_HOSTS = ls.get('ALLOWED_HOSTS', ['*'])

SILENCED_SYSTEM_CHECKS = []

SITE_ID = ls.get('SITE_ID', 1)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': ls.get('DB_NAME', ''),
        'USER': ls.get('DB_USER', ''),
        'PASSWORD': ls.get('DB_PASS', ''),
        'HOST': ls.get('DB_HOST', 'localhost'),
        'PORT': ls.get('DB_PORT', '5432'),
    }
}

DEFAULT_REDIS_HOST = ls.get('DEFAULT_REDIS_HOST', 'localhost')
DEFAULT_REDIS_PORT = ls.get('DEFAULT_REDIS_PORT', 6379)
DEFAULT_REDIS_PASSWORD = ls.get('DEFAULT_REDIS_PASSWORD', None)

REDIS_DATABASES = {
    'cache': {
        'HOST': ls.get('CACHE_REDIS_HOST', DEFAULT_REDIS_HOST),
        'PORT': ls.get('CACHE_REDIS_PORT', DEFAULT_REDIS_PORT),
        'DB': ls.get('CACHE_REDIS_DB', 1),
        'PASSWORD': ls.get('CACHE_REDIS_PASSWORD', DEFAULT_REDIS_PASSWORD),
    },
    'sessions': {
        'HOST': ls.get('SESSION_REDIS_HOST', DEFAULT_REDIS_HOST),
        'PORT': ls.get('SESSION_REDIS_PORT', DEFAULT_REDIS_PORT),
        'DB': ls.get('SESSION_REDIS_DB', 2),
        'PASSWORD': ls.get('SESSION_REDIS_PASSWORD', DEFAULT_REDIS_PASSWORD),
    },
    # 'kvdb': {
    #     'HOST': ls.get('KVDB_REDIS_HOST', DEFAULT_REDIS_HOST),
    #     'PORT': ls.get('KVDB_REDIS_PORT', DEFAULT_REDIS_PORT),
    #     'DB': ls.get('KVDB_REDIS_DB', 3),
    #     'PASSWORD': ls.get('KVDB_REDIS_PASSWORD', DEFAULT_REDIS_PASSWORD),
    # },
}


def update_caches(_caches, cache_enabled):
    def redis_pwd_prefix(cfg):
        return '{}@'.format(cfg['PASSWORD']) if cfg['PASSWORD'] else ''

    if cache_enabled:
        _CACHE_DEFAULT = {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': 'redis://{pwd}{r[HOST]}:{r[PORT]}/{r[DB]}'.format(
                pwd=redis_pwd_prefix(REDIS_DATABASES['cache']), r=REDIS_DATABASES['cache']
            ),
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                'SERIALIZER': 'django_redis.serializers.pickle.PickleSerializer',
            },
            'TIMEOUT': ls.get('CACHE_DEFAULT_TIMEOUT', 3600),
        }
    else:
        _CACHE_DEFAULT = {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }

    _caches.clear()
    _caches.update({
        'default': _CACHE_DEFAULT,
        'sessions': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': 'redis://{pwd}{r[HOST]}:{r[PORT]}/{r[DB]}'.format(
                pwd=redis_pwd_prefix(REDIS_DATABASES['sessions']), r=REDIS_DATABASES['sessions']
            ),
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                'SERIALIZER': 'core.serializers.ExtendedMSGPackSerializer',
            },
        },
        # 'kvdb': {
        #     'BACKEND': 'django_redis.cache.RedisCache',
        #     'LOCATION': 'redis://{pwd}{r[HOST]}:{r[PORT]}/{r[DB]}'.format(
        #         pwd=redis_pwd_prefix(REDIS_DATABASES['kvdb']), r=REDIS_DATABASES['kvdb']
        #     ),
        #     'OPTIONS': {
        #         'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        #         'SERIALIZER': 'django_redis.serializers.pickle.PickleSerializer',
        #     },
        #     'TIMEOUT': None,  # persistent storage
        # },
    })


CACHES = {}

update_caches(CACHES, CACHE_ENABLED)

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'sessions'
SESSION_COOKIE_AGE = 3 * 30 * 24 * 3600

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
SESSION_SERIALIZER = 'core.serializers.ExtendedMSGPackSerializer'

TIME_ZONE = ls.get('TIME_ZONE', 'Europe/Kiev')
LANGUAGE_CODE = ls.get('LANGUAGE_CODE', 'en')

# LOCALE_PATHS = [BASE_DIR.child('locale')]

# FORMAT_MODULE_PATH = ('core.formats',)

LANGUAGES = (
    ('en', 'English'),
)

USE_I18N = True
USE_L10N = True
USE_TZ = True

SECRET_KEY = ls.get('SECRET_KEY', '')

AUTH_USER_MODEL = 'userauth.User'
AUTHENTICATION_BACKENDS = [
    'apps.userauth.backends.UserModelBackend',
]
MODEL_AUTHENTICATION_BACKEND_IX = 0

INSTALLED_APPS = [
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'core',
    'apps.userauth.apps.UserauthConfig',
    'apps.citynav.apps.CityNavConfig',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR.child('templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.csrf',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]

MEDIA_ROOT = ROOT_DIR.child('var', 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = ROOT_DIR.child('var', 'static')
STATIC_URL = '/static/'

_STATICFILES_DIRS = [BASE_DIR.child('static')]
# for PyCharm
STATICFILES_DIRS = [os.path.abspath(os.path.normpath(os.path.join(os.path.dirname(__file__), os.pardir, 'static')))]
assert set(map(str, _STATICFILES_DIRS)) == set(STATICFILES_DIRS)

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

DEBUG_TOOLBAR_PANELS = [
    'ddt_request_history.panels.request_history.RequestHistoryPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]
DEBUG_TOOLBAR_CONFIG = {
    'EXTRA_SIGNALS': [
        # add custom signals for tracking
    ],
    'DISABLE_PANELS': [
        'ddt_request_history.panels.request_history.RequestHistoryPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'RESULTS_CACHE_SIZE': 100,
    'SHOW_TOOLBAR_CALLBACK': 'core.tools.show_debug_toolbar',
}

TESTING = len(sys.argv) > 1 and sys.argv[1] == 'test'

if DEBUG and not TESTING:
    TEMPLATES[0]['OPTIONS']['context_processors'].append('django.template.context_processors.debug')
    INSTALLED_APPS.insert(INSTALLED_APPS.index('django.contrib.staticfiles') + 1, 'debug_toolbar')
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
    AUTH_PASSWORD_VALIDATORS = []

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
if ls.get('EMAIL_DEBUG', DEBUG):
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    EMAIL_HOST_USER = 'debug@navsys.local'
    EMAIL_HOST_PASSWORD = ''
else:
    EMAIL_HOST = ls.get('EMAIL_HOST', 'localhost')
    EMAIL_PORT = ls.get('EMAIL_PORT', '25')
    EMAIL_USE_TLS = ls.get('EMAIL_USE_TLS', False)
    EMAIL_HOST_USER = ls.get('EMAIL_HOST_USER', 'no.reply@navsys.local')
    EMAIL_HOST_PASSWORD = ls.get('EMAIL_HOST_PASSWORD', '')
EMAIL_SUBJECT_PREFIX = ls.get('EMAIL_SUBJECT_PREFIX', 'NavSys: ')
DEFAULT_FROM_EMAIL = ls.get('DEFAULT_FROM_EMAIL', f'NavSys <{EMAIL_HOST_USER}>')
SERVER_EMAIL = ls.get('SERVER_EMAIL', DEFAULT_FROM_EMAIL)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[%(server_time)s] %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'console_error': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'logging.StreamHandler',
        },
        'console_debug': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'debug_log_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': str(LOG_DIR.child('debug.log')),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'console_error', 'mail_admins'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.template': {
            'handlers': ['console_debug'],
            'level': 'DEBUG',
            'propagate': False,
        },
        # 'django.db.backends': {
        #     'level': 'DEBUG',
        #     'handlers': ['console_debug'],
        # },
    }
}
