# vehicles/serializers/vehicle_serializer.py

import re
from rest_framework import serializers
from ..models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Vehicle
        fields = [
            "id",
            "owner",
            "owner_username",
            "make",
            "model",
            "year",
            "license_plate",
            "vehicle_type",
            "fuel_type",
            "image",
            "bluebook",
        ]
        read_only_fields = ['id']

    def validate_owner(self, value):
        # Ensure the referenced user actually exists
        # (ForeignKey already enforces this at DB level but good to have a clear error)
        return value

    def validate_year(self, value):
        import datetime
        current_year = datetime.date.today().year
        if value < 1900 or value > current_year + 1:
            raise serializers.ValidationError(
                f"Year must be between 1900 and {current_year + 1}."
            )
        return value

    def validate_license_plate(self, value):
        if not value:
            return value
        value = value.upper().strip()
        qs = Vehicle.objects.filter(license_plate=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This license plate is already registered.")
        return value

    def validate_bluebook(self, value):
        if not value:
            return value
        # Accept only PDF files
        if not value.name.lower().endswith('.pdf'):
            raise serializers.ValidationError("Bluebook must be a PDF file.")
        # Max 5 MB
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("Bluebook file must be under 5 MB.")
        return value

    def validate_image(self, value):
        if not value:
            return value
        allowed = ['.jpg', '.jpeg', '.png', '.webp']
        ext = '.' + value.name.lower().split('.')[-1]
        if ext not in allowed:
            raise serializers.ValidationError("Image must be JPG, PNG, or WEBP.")
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("Image must be under 5 MB.")
        return value