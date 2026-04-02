# users/serializers/register_serializer.py

import re
from rest_framework import serializers
from ..models import User


class RegisterSerializer(serializers.ModelSerializer):
    password         = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
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
        # Optional — only validate if provided
        if not value:
            return value
        if not re.match(r'^[\d\+\-\s\(\)]+$', value):
            raise serializers.ValidationError("Phone number contains invalid characters.")
        digits = sum(c.isdigit() for c in value)
        if digits < 7:
            raise serializers.ValidationError("Phone number must contain at least 7 digits.")
        return value  # no uniqueness check — landline can be shared

    def validate_mobile_number(self, value):
        # Required and must be unique
        if not value or not value.strip():
            raise serializers.ValidationError("Mobile number is required.")
        if not re.match(r'^[\d\+\-\s\(\)]+$', value):
            raise serializers.ValidationError("Mobile number contains invalid characters.")
        digits = sum(c.isdigit() for c in value)
        if digits < 10:
            raise serializers.ValidationError("Mobile number must contain at least 10 digits.")
        if User.objects.filter(mobile_number=value).exists():
            raise serializers.ValidationError("This mobile number is already in use.")
        return value

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({
                'confirm_password': "Passwords do not match."
            })
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user