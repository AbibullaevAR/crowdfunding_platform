from django.core.exceptions import ValidationError
from django.conf import settings

from project_management.models import Project


def like_project(project: Project, user):

    if project.taken_likes.filter(id=user.id).exists():
        project.taken_likes.remove(user)
    else:
        project.taken_likes.add(user)


def check_project_by_user_limit(user) -> bool:

    status_dict = dict(Project.STATUS_CHOICES)
    status_value = status_dict.get('waiting')

    return len(Project.objects.filter(author=user, status=status_value).all()) < settings.MAX_USER_PROJECT
    