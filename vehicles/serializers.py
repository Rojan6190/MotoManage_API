# vehicles/serializers.py
from rest_framework import serializers
from .models import Vehicle, Insurance

class VehicleSerializer(serializers.ModelSerializer):
    # Read-only fields
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
            "vehicle_type",
            "fuel_type",
            "image", #added
    
        ]
        read_only_fields = ['id']

def Validate_owner(self, value):
    pass


class InsuranceSerializer(serializers.ModelSerializer):
   
    owner_id = serializers.IntegerField(source='vehicle.owner.id', read_only=True)
    owner_username = serializers.CharField(source='vehicle.owner.username', read_only=True)
    
    class Meta:
        model = Insurance
        fields = [
            "id",
            "vehicle",
            "owner_id",           #  New
            "owner_username",      # New
            "policy_number",
            "start_date",
            "expiry_date",
            "status",
            
        ]
    

