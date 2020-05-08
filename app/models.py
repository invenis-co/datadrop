import os
import uuid
from datetime import datetime, timezone

from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver


def get_utc_now() -> datetime:
    """Return the current UTC time when called."""
    return datetime.now(timezone.utc)


class Link(models.Model):
    """Class to define a customer and generate a link to upload its files"""
    uuid = models.CharField(
        max_length=64,
        verbose_name="uuid"
    )
    email = models.CharField(
        max_length=64,
        verbose_name="email address",
        help_text='Optional',
        blank=True, null=True, db_index=True
    )
    company = models.CharField(
        max_length=64,
        verbose_name='company',
        help_text='Optional',
        blank=True, null=True, db_index=True
    )
    first_name = models.CharField(
        max_length=64,
        verbose_name='last name',
        help_text='Optional',
        blank=True, null=True, db_index=True
    )
    last_name = models.CharField(
        max_length=64,
        verbose_name='first name',
        help_text='Optional',
        blank=True, null=True, db_index=True
    )
    created_at = models.DateTimeField(
        default=get_utc_now,
        help_text='Date in format ISO8601. Example: 2020-03-03T18:31:01.915000Z.'
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        help_text='User that created the link'
    )
    enabled = models.BooleanField(
        verbose_name='Link enabled',
        default=True
    )

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(force_insert, force_update, using, update_fields)


class Upload(models.Model):
    """ Model for uploaded file for non-logged used """
    link = models.ForeignKey(
        Link,
        on_delete=models.PROTECT,
        help_text='Link given for this upload',
    )
    file = models.FileField(
        verbose_name='File to upload',
        help_text='Select one or more files to upload'
    )
    created_at = models.DateTimeField(
        default=get_utc_now,
        help_text='Date in format ISO8601. Example: 2020-03-03T18:31:01.915000Z.'
    )


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
