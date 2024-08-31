from django.contrib import admin
from .models import CameraDevice, CarEntries,CarsOwner,Permission,Car
# Register your models here.

class MyModelAdmin(admin.ModelAdmin):
    search_fields = ('id',)  # Fields to be searchable in the admin panel

# Register the model and its admin configuration
admin.site.register(CameraDevice, MyModelAdmin)
admin.site.register(CarEntries, MyModelAdmin)
admin.site.register(CarsOwner, MyModelAdmin)
admin.site.register(Permission, MyModelAdmin)
admin.site.register(Car, MyModelAdmin)

