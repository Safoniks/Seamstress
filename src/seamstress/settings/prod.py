import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# DEBUG = False
DEBUG = True

ALLOWED_HOSTS = ['seamstress.dev']

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.IsAdminUser',
    ),
    'PAGE_SIZE': 20
}

POSTGRES_USER = os.getenv('POSTGRES_USER') if os.getenv('POSTGRES_USER') else 'postgres'
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD') if os.getenv('POSTGRES_PASSWORD') else 'postgres'
POSTGRESQL_DB = os.getenv('POSTGRESQL_DB') if os.getenv('POSTGRESQL_DB') else 'postgresql'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'seamstress',
        'USER': POSTGRES_USER,
        'PASSWORD': POSTGRES_PASSWORD,
        'HOST': POSTGRESQL_DB,
        'PORT': '5432',
    }
}

# REDIS related settings
REDIS_HOST = os.getenv('REDIS_HOST') if os.getenv('REDIS_HOST') else 'localhost'
REDIS_PORT = os.getenv('REDIS_PORT') if os.getenv('REDIS_PORT') else '6379'
BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'valera.safonik@gmail.com'
EMAIL_HOST_PASSWORD = ''
