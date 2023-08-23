import os
import uuid

from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models

User = get_user_model()


def get_upload_path(instance, filename):
    return os.path.join(
        f'{instance.user_id}',
        f'{uuid.uuid4()}{filename}'
    )


class StatusType(models.TextChoices):
    NEW = 'new'
    MODIFIED = 'modified'
    CHECKED = 'checked'
    FAILED = 'failed'


class File(models.Model):
    name = models.CharField(max_length=40, blank=False)
    status = models.CharField(choices=StatusType.choices)
    file = models.FileField(
        upload_to=get_upload_path,
        validators=[
            FileExtensionValidator(allowed_extensions=['py'])
        ]
    )

    start_datetime = models.DateTimeField(blank=False)
    period = models.TimeField(blank=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
