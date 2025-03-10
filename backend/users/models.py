from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _
from django.conf import settings

class Role(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    role = models.ForeignKey(
        Role, on_delete=models.SET_NULL, null=True, blank=True
    )
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        if self.first_name:
            return self.first_name + " " + self.last_name
        return self.username 
