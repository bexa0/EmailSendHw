from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Key(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=8)

    def __str__(self):
        return self.key