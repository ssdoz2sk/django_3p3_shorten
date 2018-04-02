from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class ShortenUser(AbstractUser):
    is_banned = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name

