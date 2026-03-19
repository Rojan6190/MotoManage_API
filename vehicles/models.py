from django.db import models
from core.models import BaseModel
from django.conf import settings
class Vehicle(BaseModel):
    VEHICLE_TYPE =[
        ("two_wheeler","Two Wheeler"),
        ("four_wheeler","Four Wheeler"),
        ("heavy","Heavy Vehicle"),
    ]

    FUEL_TYPE =[
        ("petrol","Petrol"),
        ("diesel","Diesel"),
        ("electric","Electric"),
    ]

    owner = models.ForeignKey(  
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='vehicles'
    )
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveBigIntegerField()
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPE)
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPE, default='petrol')

class Insurance(BaseModel):
    STATUS_CHOICES = [         #later use class-based enums instead of choice tuples
        ("active","Active"),
        ("expired","Expired"),
        ("pending","Pending"),
    ]

    vehicle = models.OneToOneField(Vehicle, on_delete=models.CASCADE, related_name='insurance')
    policy_number = models.CharField(max_length=50, unique=True)
    start_date = models.DateField()
    expiry_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

