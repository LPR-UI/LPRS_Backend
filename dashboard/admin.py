from django.contrib import admin
from .models import Permission, Camera,Car,CarEntry,CarOwner
# Register your models here.

class MyModelAdmin(admin.ModelAdmin):
    search_fields = ('id',)  # Fields to be searchable in the admin panel

# Register the model and its admin configuration
admin.site.register(Camera, MyModelAdmin)
admin.site.register(CarEntry, MyModelAdmin)
admin.site.register(CarOwner, MyModelAdmin)
admin.site.register(Permission, MyModelAdmin)
admin.site.register(Car, MyModelAdmin)

