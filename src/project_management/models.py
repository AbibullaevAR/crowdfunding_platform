import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

# Create your models here.

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(_('name'), max_length=60, blank=False)

    projects = models.ManyToManyField('Project', through='ProjectCategory')


class Project(models.Model):

    STATUS_CHOICES = (
        ('approve', 'approve'),
        ('cancel', 'cancel'),
        ('waiting', 'waiting')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(_('title'), max_length=45, blank=False)
    goal_likes = models.PositiveIntegerField(_('goal_likes'), default=0, blank=False)
    short_description = models.CharField(_('short_description'), max_length=250)
    description = models.TextField(_('description'), blank=False)
    start_project = models.DateField(blank=False)
    end_project = models.DateField(blank=False)
    status = models.CharField(_('status'), max_length=10, choices=STATUS_CHOICES, default='waiting')

    categories = models.ManyToManyField(Category, through='ProjectCategory')
    taken_likes = models.ManyToManyField(get_user_model(), through='UserProjectLike')

    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='projects', blank=False)

    
    def taken_likes_count(self) -> int:
        return self.taken_likes.count()


class ProjectCategory(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('project', 'category')


class UserProjectLike(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        unique_together = ('project', 'user')


class Comment(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    text = models.CharField(max_length=250, blank=False)
    created_at = models.DateField(auto_now_add=True)

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
