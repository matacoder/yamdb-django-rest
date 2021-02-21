from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from .managers import UserManager


class User(AbstractUser):
    """ Custom YamDB user with email authentication"""

    class RoleChoice(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    email = models.EmailField(
        verbose_name='email address', max_length=150, unique=True
    )
    username = models.CharField(
        max_length=150, unique=True,
        blank=True, null=True,
        validators=(UnicodeUsernameValidator,)
    )
    bio = models.TextField(
        verbose_name='biography', blank=True
    )
    role = models.CharField(
        max_length=25, choices=RoleChoice.choices,
        default=RoleChoice.USER
    )

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def is_admin(self):
        return self.role == self.RoleChoice.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.RoleChoice.MODERATOR

    class Meta:
        ordering = ['-id']
