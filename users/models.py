# users/models.py

from django.db import models
from core.models import BaseModel
from django.contrib.auth.models import AbstractUser


class User(AbstractUser, BaseModel):
    username     = models.CharField(max_length=15, unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    age          = models.PositiveBigIntegerField(null=True)
    mobile_number = models.CharField(max_length=20, unique=False, default="+977-9800000000")
    address      = models.CharField(max_length=100, null=True)

    GENDER_CHOICE = [
        ("male",   "Male"),
        ("female", "Female"),
        ("other",  "Other"),
    ]
    gender = models.CharField(max_length=20, choices=GENDER_CHOICE, default="male")

    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("user",  "User"),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="user")

    def __str__(self):
        return self.username