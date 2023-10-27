from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone_number = models.CharField(max_length=20)

    def get_fullname(self):
        return self.first_name + self.last_name
