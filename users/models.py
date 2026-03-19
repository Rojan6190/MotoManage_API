from django.db import models
from core.models import BaseModel
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser, BaseModel):
    username = models.CharField(max_length=15, unique= True)
    phone_number = models.CharField(max_length=15, unique=True)
    age = models.PositiveBigIntegerField(null=True)
    mobile_number = models.CharField(max_length=100,unique=False, default="+977-9800000000")
    address = models.CharField(max_length=100, null=True)
    
    GENDER_CHOICE = [
        ("male","Male"),
        ("female","Female"),
        ("other","Other"),
    ]
    
    gender = models.CharField(max_length=20, choices=GENDER_CHOICE, default="male")

