# from .settings import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'cusse',
        'USER': 'postgres',
        'PASSWORD': 'bh479832',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# INSTALLED_APPS += [
#     'django-debug-toolbar'
# ]
