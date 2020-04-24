from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone


class BaseModel(models.Model):
    """
    Abstract Base Model to be inherited. It contains created and updated fields for the classes
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Client(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    email = models.CharField(blank=True, null=True, max_length=200)
    firstname = models.CharField(blank=True, null=True, max_length=200)
    lastname = models.CharField(blank=True, null=True, max_length=200)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user)

    def staff(self):
        return self.user.is_staff

    def admin(self):
        return self.user.is_superuser

    def username(self):
        return self.user.username

