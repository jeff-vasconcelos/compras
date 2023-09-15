import os
from pathlib import Path
from environ import Env

BASE_DIR = Path(__file__).resolve().parent.parent

env = Env(
    DEBUG=(bool, False),
    SECURE_SSL_REDIRECT=(bool, False),
    SESSION_COOKIE_SECURE=(bool, False),
    CSRF_COOKIE_SECURE=(bool, False),
    CSRF_COOKIE_HTTPONLY=(bool, True),
    SESSION_COOKIE_HTTPONLY=(bool, True)
)
Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env.str('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = env.list('HOSTS')

LOGIN_URL = '/'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'api',
    'core',
    'rest_framework',
    'rest_framework.authtoken',
    'crispy_forms',
    'django_celery_beat',
    'django_crontab',
    'debug_toolbar',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'setup.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'to_str': 'core.templatetags.to_str',
            }
        },
    },
]

WSGI_APPLICATION = 'setup.wsgi.application'

CORS_ORIGIN_ALLOW_ALL = True

DATABASES = {
    'default': env.db_url('DB_URL')
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join('templates/static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    # 'DEFAULT_AUTHENTICATION_CLASSES': [
    #     'rest_framework_simplejwt.authentication.JWTAuthentication',
    # ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# SMTP CONFIGURATION
EMAIL_BACKEND = env.str('EMAIL_BACKEND')
EMAIL_HOST = env.str('EMAIL_HOST')
EMAIL_PORT = env.int('EMAIL_PORT')
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS')
EMAIL_USE_SSL = env.bool('EMAIL_USE_SSL')
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD')

# 24 horas de sessão
SESSION_COOKIE_AGE = 86400

# Salvar a cada requisição
SESSION_SAVE_EVERY_REQUEST = False

INTERNAL_IPS = [
    '127.0.0.1',
]

# CELERY STUFF
REDIS_URL = env.str('REDIS_URL')
BROKER_URL = REDIS_URL
CELERY_IMPORTS = ("core.tasks",)
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'America/Sao_Paulo'

DATA_UPLOAD_MAX_NUMBER_FIELDS = None
DATA_UPLOAD_MAX_MEMORY_SIZE = None

THOUSAND_SEPARATOR = '.',
USE_THOUSAND_SEPARATOR = True

# CONFIG SSL
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
