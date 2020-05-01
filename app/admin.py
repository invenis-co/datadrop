# pylint: disable=missing-module-docstring
from django.contrib import admin

from app.models import Download, Upload

admin.register(Upload)
admin.register(Download)
