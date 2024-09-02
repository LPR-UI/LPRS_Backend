from rest_framework import serializers
from django.core.validators import RegexValidator
from .models import CarOwner

class CarOwnerSerializer(serializers.ModelSerializer):
    firstName = serializers.CharField(
        max_length=50, 
        validators=[
            RegexValidator(regex=r'^[a-zA-Z]+$', message='First name must contain only letters.')
        ]
    )
    lastName = serializers.CharField(
        max_length=50, 
        validators=[
            RegexValidator(regex=r'^[a-zA-Z]+$', message='Last name must contain only letters.')
        ]
    )
    nationalCode = serializers.CharField(
        max_length=10, 
        validators=[
            RegexValidator(regex=r'^\d{10}$', message='National code must be exactly 10 digits.')
        ]
    )
    phoneNumber = serializers.CharField(
        max_length=11, 
        validators=[
            RegexValidator(regex=r'^09\d{9}$', message='Phone number must start with 09 and be exactly 11 digits.')
        ]
    )
    career = serializers.CharField(
        max_length=50, 
        validators=[
            RegexValidator(regex=r'^[a-zA-Z]+$', message='Career must contain only letters.')
        ]
    )

    class Meta:
        model = CarOwner
        fields = '__all__'
