from django.contrib import admin
from .models import Region, City


class RegionAdmin(admin.ModelAdmin):
    list_display = ['name',]


class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'region', 'people']


admin.site.register(Region, RegionAdmin)
admin.site.register(City, CityAdmin)