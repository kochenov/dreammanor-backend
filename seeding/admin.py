from django.contrib import admin

from .models import *


class VegetableAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'description')


class VegetableSortAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'vegetable')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'description')


admin.site.register(Vegetable, VegetableAdmin)
admin.site.register(VegetableSort, VegetableSortAdmin)

admin.site.site_title = 'Администрирование DreamManor'
admin.site.site_header = 'DreamManor: Панель управления'
