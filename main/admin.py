from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Hotel, HotelImage


class HotelImageInline(admin.StackedInline):
    model = HotelImage
    extra = 1


@admin.register(Hotel)
class HotelAdmin(ImportExportModelAdmin):
    list_display = ('name', 'uid', 'stars', 'deleted', 'deleted_at', 'created_at')
    list_filter = ('country', 'city', 'state')
    search_fields = ['name']
    ordering = ['name', 'created_at']
    inlines = [HotelImageInline]


@admin.register(HotelImage)
class HotelImageAdmin(admin.ModelAdmin):
    list_display = ('uid', 'hotel', 'uploaded')
    list_filter = ['hotel']