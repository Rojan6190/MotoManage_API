from rest_framework import serializers
from ..models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only = True)
    class Meta:
        model = User
        fields=[
            'username',
            'email',
            'password',
            'confirm_password',
            'first_name',
            'last_name',
            'phone_number',
            'mobile_number',
            'age',
            'address',
            'gender',
        ]
    def validate_age(self, value):
        if value is not None and value < 18:
            raise serializers.ValidationError("Age must be 18 or above!")
        return value
 
    def validate_username(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Username too short!")
        return value
 
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
 
    def validate_phone_number(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Phone number must be at least 10 digits.")
        return value
    
    def validate(self, data):
        """
        Cross-field validation — runs after all individual field validators.
        This is the right place to compare password and confirm_password
        since both fields need to be present at the same time.
        """
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({
                'confirm_password': "Passwords do not match."
            })
        return data

 
    def create(self, validated_data):
        # Remove confirm_password — it's not a model field
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
 