from .settings import *

DEBUG = False

# Security
ALLOWED_HOSTS = ['localhost', 'YOUR_SITE']
CSRF_TRUSTED_ORIGINS = ['YOUR_SITE']
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
SECRET_KEY = 'ADD YOUR PRODUCTION SECRET KEY HERE'  # nosec

# Database
DATABASES['default']['NAME'] = os.path.join('/data', 'db.sqlite3')

# Mail configuration
ADMINS = [('NAME', 'MAIL'), ]
EMAIL_SUBJECT_PREFIX = '[Datadrop]'
SERVER_EMAIL = 'FROM_MAIL_FOR_ERROR'
DEFAULT_FROM_EMAIL = 'FROM_MAIL_FOR_ADMIN_LIKE_RESET_PASSWORD'
EMAIL_HOST = ''
EMAIL_PORT = 465
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''  # nosec
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_TIMEOUT = 10

STATIC_ROOT = '/static'
MEDIA_ROOT = '/uploads'
