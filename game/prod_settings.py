from .settings import *

import dj_datebase_url
DATABASES = {
    'default': dj_datebase_url.config()
}
STATIC_ROOT = 'staticfiles'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
ALLOWED_HOSTS = ['*']
DEBUG = False
