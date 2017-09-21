import os
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SECRET_KEY = 'mj%gnq3$!28z9uwr2t(t^lxbdmhnp0t7f(*!o2!zs_b$2%ttja'


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'simple_history',
    'rest_framework',
    'rest_framework_swagger',

    'product.apps.ProductConfig',
    'operation.apps.OperationConfig',
    'operationtype.apps.OperationtypeConfig',
    'operationtypecategory.apps.OperationtypecategoryConfig',
    'worker.apps.WorkerConfig',
    'user.apps.UserConfig',
    'brigade.apps.BrigadeConfig',
    'public.apps.PublicConfig'
]


JWT_AUTH = {
    'JWT_ENCODE_HANDLER': 'rest_framework_jwt.utils.jwt_encode_handler',
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'custom_jwt.jwt_response_payload_handler',
    'JWT_PAYLOAD_HANDLER': 'custom_jwt.jwt_payload_handler',
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=10)
}

MIDDLEWARE = [
    'simple_history.middleware.HistoryRequestMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'seamstress.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'seamstress.wsgi.application'


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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static/')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'media/')
PRODUCT_PHOTOS_DIR_NAME = 'product-photos'

SERVER_EMAIL = 'root@localhost'
DEFAULT_FROM_EMAIL = 'webmaster@localhost'

INITIAL_DIRECTOR = {
    'username': 'director',
    'password': 'director',
    'email': 'director@director',
}


APPLICATION_SETTINGS = {
    'salary_days': 7,
    'working_hours': 8,
}


if os.getenv('DJANGO_ENV') == 'prod':
    from .prod import *
else:
    from .dev import *
