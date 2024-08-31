from django.db import models

class CarEntry(models.Model):
    license_plate = models.ForeignKey('Car', on_delete=models.CASCADE)
    camera = models.ForeignKey('Camera', on_delete=models.CASCADE)
    timestamp = models.DateTimeField()

class Car(models.Model):
    license_plate = models.CharField(max_length=8, unique=True, primary_key=True)
    owner = models.ForeignKey('CarOwner', on_delete=models.CASCADE)
    color = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CarOwner(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    nationalCode = models.CharField(max_length=10, unique=True)
    phoneNumber = models.CharField(max_length=11, unique=True)
    dateOfBirth = models.DateField()
    career = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Camera(models.Model):
    class CameraLevel(models.IntegerChoices):
        FULL_ACCESS = 1, "Full Access"
        STAFF = 2, "Limited Access"
        GUEST = 3, "Guest"

    location = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    is_entry_camera = models.BooleanField(default=False)
    level = models.IntegerField(choices=CameraLevel.choices,
                                default=CameraLevel.GUEST)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Permission(models.Model):
    class PermissionLevel(models.IntegerChoices):
        FULL_ACCESS = 1, "Full Access"
        STAFF = 2, "Limited Access"
        GUEST = 3, "Guest"

    license_plate = models.ForeignKey('Car', on_delete=models.CASCADE)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    isAllowed = models.BooleanField(default=True)
    level = models.IntegerField(choices=PermissionLevel.choices,
                                default=PermissionLevel.GUEST)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)