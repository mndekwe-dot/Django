import os
from .common import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False 

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get['SECRET_KEY']


ALLOWED_HOSTS = []