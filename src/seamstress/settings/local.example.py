import os
from .main import BASE_DIR, REST_FRAMEWORK

DEBUG = True

ALLOWED_HOSTS = ['*']

SECRET_KEY = 'YOUR_KEY'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db_name',
        'USER': 'db_user',
        'PASSWORD': 'password',
        'HOST': 'db_host',
        'PORT': 'db_port',  # default 5432
    }
}

# REDIS related settings
BROKER_URL = 'redis://REDIS_HOST:REDIS_PORT/0'  # for ex. REDIS_HOST = localhost, REDIS_PORT = 6379
                                                # url = 'redis://localhost:6379/0'
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = BROKER_URL

# email settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'example@gmail.com'
EMAIL_HOST_PASSWORD = 'password'
