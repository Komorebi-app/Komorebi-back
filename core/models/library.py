from django.contrib.auth.models import User
from django.db import models

class Library(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user.get_full_name())
