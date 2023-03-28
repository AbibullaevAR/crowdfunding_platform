import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone

# Create your models here.

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(_('name'), max_length=60, blank=False)

    projects = models.ManyToManyField('Project', through='ProjectCategory')


class Project(models.Model):

    STATUS_CHOICES = (
        ('AP', 'approve'),
        ('CL', 'cancel'),
        ('WT', 'waiting')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(_('title'), max_length=45, blank=False)
    goal_likes = models.PositiveIntegerField(_('goal_likes'), default=0, blank=False)
    taken_likes = models.PositiveIntegerField(_('taken_likes'), default=0, blank=False)
    short_description = models.CharField(_('short_description'), max_length=180)
    start_project = models.DateField(blank=False)
    end_project = models.DateField(blank=False)
    status = models.CharField(_('status'), max_length=2, choices=STATUS_CHOICES, default='WT')

    categories = models.ManyToManyField(Category, through='ProjectCategory')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='projects', blank=False)

    def clean(self) -> None:
        if self.start_project < timezone.localdate():
            raise ValidationError(_('Start date should be greater or equal to current date.'))
        if self.start_project > self.end_project:
            raise ValidationError(_('End date should be greater or equal to start date.'))


class ProjectCategory(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('project', 'category')