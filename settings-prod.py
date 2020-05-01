from .settings import *

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

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
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_TIMEOUT = 10

STATIC_ROOT = '/static'
MEDIA_ROOT = '/uploads'
