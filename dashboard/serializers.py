from rest_framework import serializers
from django.core.validators import RegexValidator
from .models import CarOwner, Car
import jdatetime

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


class ListAllCarOwnerSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    birthdate = serializers.SerializerMethodField()

    class Meta:
        model = CarOwner
        fields = ['id', 'full_name', 'nationalCode', 'phoneNumber', 'birthdate', 'career']

    def get_full_name(self, obj):
        return f"{obj.firstName} {obj.lastName}"
    
    def get_birthdate(self, obj):
        return jdatetime.datetime.fromgregorian(date=obj.dateOfBirth).strftime('%Y-%m-%d')
    
# class Car(models.Model):
#     license_plate = models.CharField(max_length=10, unique=True, primary_key=True)
#     owner = models.ForeignKey('CarOwner', on_delete=models.CASCADE)
#     color = models.CharField(max_length=50)
#     model = models.CharField(max_length=50)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
class ListAllCarOwnerSerializer(serializers.ModelSerializer):
    owner_id = serializers.SerializerMethodField()
    owner_name = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = ['license_plate', 'owner_id', 'owner_name', 'model', 'color']

    def get_owner_id(self, obj):
        return obj.owner.id

    def get_owner_name(self, obj):
        return f"{obj.owner.firstName} {obj.owner.lastName}"
