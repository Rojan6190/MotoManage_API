# vehicles/serializers/insurance_serializer.py

from rest_framework import serializers
from ..models import Insurance


class InsuranceSerializer(serializers.ModelSerializer):
    owner_id       = serializers.IntegerField(source='vehicle.owner.id',       read_only=True)
    owner_username = serializers.CharField(source='vehicle.owner.username',    read_only=True)

    class Meta:
        model = Insurance
        fields = [
            "id",
            "vehicle",
            "owner_id",
            "owner_username",
            "policy_number",
            "start_date",
            "expiry_date",
            "status",
            "document",
        ]

    def validate_document(self, value):
        if not value:
            return value
        # Accept only PDF files
        if not value.name.lower().endswith('.pdf'):
            raise serializers.ValidationError("Insurance document must be a PDF file.")
        # Max 5 MB
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("Document file must be under 5 MB.")
        return value

    def validate(self, data):
        # Cross-field: expiry must be after start
        start  = data.get('start_date')
        expiry = data.get('expiry_date')
        if start and expiry and expiry <= start:
            raise serializers.ValidationError({
                'expiry_date': "Expiry date must be after the start date."
            })
        return data