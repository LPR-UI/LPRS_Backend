import re
from rest_framework import serializers
from django.core.validators import RegexValidator
from .models import CarOwner, Car, Permission, Camera
import jdatetime
from django.utils import timezone
from datetime import datetime


# ADD
# TODO: Check if it is not a duplicate
# TODO: What happens if there is a permission in the database?
class CarOwnerSerializer(serializers.ModelSerializer):
    firstName = serializers.CharField(
        max_length=50, 
        validators=[
            RegexValidator(regex=r'^[a-zA-Z\u0600-\u06FF\s]+$', message='First name must contain only letters (English or Persian).')
        ]
    )
    lastName = serializers.CharField(
        max_length=50, 
        validators=[
            RegexValidator(regex=r'^[a-zA-Z\u0600-\u06FF\s]+$', message='Last name must contain only letters (English or Persian).')
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
            RegexValidator(regex=r'^[a-zA-Z\u0600-\u06FF\s]+$', message='Career must contain only letters (English or Persian).')
        ]
    )
    dateOfBirth = serializers.CharField()

    class Meta:
        model = CarOwner
        fields = '__all__'

    def validate(self, data):
        # Convert Jalali date to Gregorian date
        date_str = data.get('dateOfBirth')
        if date_str:
            try:
                jalali_date = jdatetime.datetime.strptime(date_str, '%Y-%m-%d')
                gregorian_date = jalali_date.togregorian().date()
                data['dateOfBirth'] = timezone.make_aware(datetime.combine(gregorian_date, datetime.min.time()), timezone.get_current_timezone())
            except ValueError:
                raise serializers.ValidationError({'dateOfBirth': "Invalid Jalali date format. Use YYYY-MM-DD."})
  
        return data

class CarSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=CarOwner.objects.all())
    model = serializers.CharField(max_length=50)
    license_plate = serializers.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\d{2}[a-zA-Z]{2,8}\d{5}$',
                message='License plate must follow the format: two digits, 2 to 8 letters, five digits.'
            )
        ]
    )
    color = serializers.CharField(
        max_length=30,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z\u0600-\u06FF\s]+$',
                message='Color must contain only letters (English or Persian).'
            )
        ]
    )

    class Meta:
        model = Car
        fields = ['owner', 'model', 'license_plate', 'color']

class GetOwnersInCarCreationSerializer(serializers.ModelSerializer):
    value = serializers.IntegerField(source='id')
    name = serializers.SerializerMethodField()

    class Meta:
        model = CarOwner
        fields = ['value', 'name']

    def get_name(self, obj):
        return f"{obj.firstName} {obj.lastName} ({obj.id})"

class PermissionSerializer(serializers.ModelSerializer):
    license_plate = serializers.CharField(max_length=15)
    start_date = serializers.CharField()
    end_date = serializers.CharField()
    level = serializers.IntegerField(min_value=1, max_value=3)
    is_allowed = serializers.BooleanField()

    class Meta:
        model = Permission
        fields = ['license_plate', 'start_date', 'end_date', 'level', 'is_allowed']

    def validate_license_plate(self, value):
        if not re.match(r'^\d{2}[A-Za-z]{2,8}\d{5}$', value):
            raise serializers.ValidationError("License plate must be in the format: two digits, 2-8 letters, four digits.")
        return value

    def validate(self, data):
        # Convert Jalali date to Gregorian date
        for date_field in ['start_date', 'end_date']:
            date_str = data.get(date_field)
            if date_str:
                try:
                    jalali_date = jdatetime.datetime.strptime(date_str, '%Y-%m-%d')
                    gregorian_date = jalali_date.togregorian().date()
                    data[date_field] = timezone.make_aware(datetime.combine(gregorian_date, datetime.min.time()), timezone.get_current_timezone())
                except ValueError:
                    raise serializers.ValidationError({date_field: "Invalid Jalali date format. Use YYYY-MM-DD."})

        # Check that end_date is after start_date
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError("End date must be after the start date.")
        
        return data

    def create(self, validated_data):
        license_plate = validated_data.pop('license_plate')
        try:
            car = Car.objects.get(license_plate=license_plate)
        except Car.DoesNotExist:
            raise serializers.ValidationError(f"Car with license plate {license_plate} does not exist.")
        
        permission = Permission.objects.create(license_plate=car, **validated_data)
        return permission

    def create(self, validated_data):
        # Handle creation logic including resolving the license plate to a Car instance
        license_plate = validated_data.pop('license_plate')
        try:
            car = Car.objects.get(license_plate=license_plate)
        except Car.DoesNotExist:
            raise serializers.ValidationError(f"Car with license plate {license_plate} does not exist.")
        
        permission = Permission.objects.create(license_plate=car, **validated_data)
        return permission

    def update(self, instance, validated_data):
        # Handle update logic including resolving the license plate to a Car instance
        license_plate = validated_data.pop('license_plate', None)
        if license_plate:
            try:
                car = Car.objects.get(license_plate=license_plate)
            except Car.DoesNotExist:
                raise serializers.ValidationError(f"Car with license plate {license_plate} does not exist.")
            instance.license_plate = car

        # Update other fields
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.level = validated_data.get('level', instance.level)
        instance.is_allowed = validated_data.get('is_allowed', instance.is_allowed)

        instance.save()
        return instance
    
class GetLPsInPermissionCreationSerializer(serializers.ModelSerializer):
    value = serializers.CharField(source='license_plate')

    class Meta:
        model = Car
        fields = ['value']

class CameraSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Camera
        fields = ['location', 'description', 'level', 'is_entry_camera']    

# LISTS
class ListAllCarOwnerSerializer(serializers.ModelSerializer):
    dateOfBirth = serializers.SerializerMethodField()

    class Meta:
        model = CarOwner
        fields = ['id', 'firstName', 'lastName', 'nationalCode', 'phoneNumber', 'dateOfBirth', 'career']

    
    def get_dateOfBirth(self, obj):
        return jdatetime.datetime.fromgregorian(date=obj.dateOfBirth).strftime('%Y-%m-%d')    

class ListAllCarSerializer(serializers.ModelSerializer):
    owner_id = serializers.SerializerMethodField()
    owner_name = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = ['license_plate', 'owner_id', 'owner_name', 'model', 'color']

    def get_owner_id(self, obj):
        return obj.owner.id

    def get_owner_name(self, obj):
        return f"{obj.owner.firstName} {obj.owner.lastName}"

class ListAllPermissionSerializer(serializers.ModelSerializer):
    start_date = serializers.SerializerMethodField()
    end_date = serializers.SerializerMethodField()

    class Meta:
        model = Permission
        fields = ['id','license_plate', 'start_date', 'end_date', 'is_allowed', 'level']

    def get_start_date(self, obj):
        return jdatetime.datetime.fromgregorian(date=obj.start_date).strftime('%Y-%m-%d')

    def get_end_date(self, obj):
        return jdatetime.datetime.fromgregorian(date=obj.end_date).strftime('%Y-%m-%d')

class ListAllCameraSerializer(serializers.ModelSerializer):

    class Meta:
        model = Camera
        fields = ['id','location', 'description', 'is_entry_camera', 'level']