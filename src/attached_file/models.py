import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from project_management.models import Project

# Create your models here.

class Image(models.Model):

    AVAILABLE_FORMAT_CHOICES = (
        ('.png', 'PNG'),
        ('.jpg', 'JPG'),
        ('.jpeg', 'JPEG')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    available_format = models.CharField(_('available_format'), max_length=5, choices=AVAILABLE_FORMAT_CHOICES, default='.jpg')

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
