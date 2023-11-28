from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class MainUser(AbstractUser):
    email = models.EmailField('Email', unique=True, null=True)

    class Meta:
        verbose_name = 'Все пользователи'
        verbose_name_plural = 'Все пользователи'