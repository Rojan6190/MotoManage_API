# vehicles/models.py

from django.db import models
from core.models import BaseModel
from django.conf import settings


class Vehicle(BaseModel):
    VEHICLE_TYPE = [
        ("two_wheeler",  "Two Wheeler"),
        ("four_wheeler", "Four Wheeler"),
        ("heavy",        "Heavy Vehicle"),
    ]

    FUEL_TYPE = [
        ("petrol",   "Petrol"),
        ("diesel",   "Diesel"),
        ("electric", "Electric"),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='vehicles'
    )
    make          = models.CharField(max_length=100)
    model         = models.CharField(max_length=100)
    year          = models.PositiveBigIntegerField()
    license_plate = models.CharField(max_length=20, unique=True, null=True, blank=True)
    vehicle_type  = models.CharField(max_length=20, choices=VEHICLE_TYPE)
    fuel_type     = models.CharField(max_length=20, choices=FUEL_TYPE, default='petrol')

    image = models.ImageField(
        upload_to='vehicles/images/',   # organized subfolder
        null=True, blank=True,
    )
    bluebook = models.FileField(
        upload_to='vehicles/documents/',
        null=True, blank=True,
    )

    def __str__(self):
        return f"{self.year} {self.make} {self.model} ({self.owner})"


class Insurance(BaseModel):
    STATUS_CHOICES = [
        ("active",  "Active"),
        ("expired", "Expired"),
        ("pending", "Pending"),
    ]

    vehicle       = models.OneToOneField(Vehicle, on_delete=models.CASCADE, related_name='insurance')
    policy_number = models.CharField(max_length=50, unique=True)
    start_date    = models.DateField()
    expiry_date   = models.DateField()
    status        = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    document = models.FileField(
        upload_to='insurance/documents/',
        null=True, blank=True,
    )

    def __str__(self):
        return f"{self.policy_number} — {self.vehicle}"