# users/serializers/user_serializer.py

import re
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
        return f"{obj.first_name or ''} {obj.last_name or ''}".strip() or obj.username

    def validate_age(self, value):
        if value is not None and value < 18:
            raise serializers.ValidationError("Age must be 18 or above!")
        return value

    def validate_username(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Username too short!")
        qs = User.objects.filter(username=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def validate_email(self, value):
        qs = User.objects.filter(email=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("User with this email already exists!")
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
        qs = User.objects.filter(mobile_number=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This mobile number is already in use.")
        return value