from rest_framework import serializers
from ..models import User

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 
            'username', 
            'email', 
            'phone_number', 
            'age',
            'first_name',
            'last_name',
            'full_name',
            'is_active',
            'date_joined',
            'mobile_number',
            'address',
            'gender',
        ]
        read_only_fields = ['id', 'date_joined', 'is_active']
    
    def get_full_name(self, obj):
        
        return f"{obj.first_name} {obj.last_name}".strip() or obj.username
    
    def validate_age(self, value):
        if value is not None and value < 18:
            raise serializers.ValidationError("Age must be 18 or above!")
        return value
    
    def validate_username(self, value):
     if len(value) < 3:
        raise serializers.ValidationError("Username too short!!")
     qs = User.objects.filter(username=value)
     if self.instance:
        qs = qs.exclude(pk=self.instance.pk)
     if qs.exists():
        raise serializers.ValidationError("This username is already taken.")
     return value
    
    def validate_email(self, value):
     qs = User.objects.filter(email=value)
     # If updating (instance exists), exclude the current user from the check
     if self.instance:
        qs = qs.exclude(pk=self.instance.pk)
     if qs.exists():
        raise serializers.ValidationError("User with this email already exists!")
     return value
    
    def validate_phone_number(self, value):
        if len(value)<10:
            raise serializers.ValidationError("Phone no must be at least 10 digits.")
        return value
    def validate_phone_number(self, value):
     if len(value) < 10:
        raise serializers.ValidationError("Phone no must be at least 10 digits.")
     qs = User.objects.filter(phone_number=value)
     if self.instance:
        qs = qs.exclude(pk=self.instance.pk)
     if qs.exists():
        raise serializers.ValidationError("This phone number is already in use.")
     return value