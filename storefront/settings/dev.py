from .common import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-$25()q9og)##h(*gb%7x5kbrynj^!2pwgotpb_084iu%)nj))="

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        'NAME': 'storefront',
        'USER': 'root',
        'HOST': '127.0.0.1',
        "PASSWORD": "mercermerc123@M",
        'PORT': '3306',
    }
}


