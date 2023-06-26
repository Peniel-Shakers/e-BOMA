from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Client(AbstractUser):
    telephone = models.CharField(max_length=20)
    adresse = models.CharField(max_length=255) 