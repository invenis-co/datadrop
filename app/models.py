import os
from datetime import datetime, timezone

from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.urls import reverse


def get_utc_now() -> datetime:
    """Return the current UTC time when called."""
    return datetime.now(timezone.utc)


class Upload(models.Model):
    """ Model for uploaded file for non-logged used """
    company = models.CharField(
        max_length=64,
        verbose_name='company name',
        help_text='Optional',
        blank=True, null=True, db_index=True
    )
    file = models.FileField(
        verbose_name='File to upload'
    )
    created_at = models.DateTimeField(
        default=get_utc_now,
        help_text='Date in format ISO8601. Example: 2020-03-03T18:31:01.915000Z.'
    )

    @staticmethod
    def get_absolute_url():
        """Return to thanks page after creation"""
        return reverse('thanks')


@receiver(models.signals.post_delete, sender=Upload)
# pylint: disable=unused-argument
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


class Download(models.Model):
    """ Model to log downloads of uploaded files """
    downloader = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        help_text='User that download the file'
    )
    upload = models.ForeignKey(
        Upload,
        on_delete=models.SET_NULL,
        null=True,
        help_text='User that uploaded the extension'
    )
    created_at = models.DateTimeField(
        default=get_utc_now,
        help_text='Date in format ISO8601. Example: 2020-03-03T18:31:01.915000Z.'
    )
