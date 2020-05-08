# pylint: disable=missing-module-docstring
from django.contrib import admin

from app.models import Download, Upload, Link

admin.site.register(Upload)
admin.site.register(Download)
admin.site.register(Link)
