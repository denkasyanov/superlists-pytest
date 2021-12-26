from django.db import models
from uuid import uuid4


class User(models.Model):
    email = models.EmailField(primary_key=True)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"
    is_anonymous = False
    is_authenticated = True


class Token(models.Model):
    uid = models.UUIDField(default=uuid4, primary_key=True)
    email = models.EmailField()
