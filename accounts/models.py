from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        if self.first_name:
            return self.first_name
        return self.username or self.email.split('@')[0]

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email
