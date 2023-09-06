from django.db import models
from django.contrib.auth.models import AbstractUser

from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.utils import BaseModel
from accounts.manager import Usermanager

import uuid




# Create your models here.

#custom user model
class User(AbstractUser):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    username = None
    phone = models.CharField(unique=True, max_length=15)
    email = models.EmailField(blank=True, null=True, default="")
    last_logout = models.DateTimeField(null=True, blank=True)
    
    objects = Usermanager()
    
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    
    class Meta:
        db_table = 'auth_user'
        verbose_name_plural = "Eco Visionaries User"
        ordering = ['date_joined']
    
    def __str__(self):
        return self.phone