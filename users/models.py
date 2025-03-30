from datetime import datetime
from typing import Any, override
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    user: models.OneToOneField[User] = models.OneToOneField(
        User, on_delete=models.CASCADE)
    # optional profile picture.
    avatar = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @override
    def __str__(self) -> str:
        return self.user.get_full_name()
