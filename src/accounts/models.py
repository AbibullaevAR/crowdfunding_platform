from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class Role(models.Model):

    class RoleInSystem(models.TextChoices):
        ADMIN = 'AD', _('Admin')
        STUDENT = 'ST', _('Student')

    role_in_system = models.CharField(
        max_length=2,
        choices=RoleInSystem.choices,
        default=RoleInSystem.STUDENT,
        blank=False
    )

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(_('name'), max_length=60, blank=False)
    is_active = models.BooleanField(_('active'), default=True)