from django.contrib import admin

from .models import *


class VegetableAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'description')


admin.site.register(Vegetable, VegetableAdmin)
