from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Hotel, HotelImage, Room, Reservation


class HotelImageInline(admin.StackedInline):
    model = HotelImage
    extra = 1


class ReservationInline(admin.TabularInline):
    model = Reservation
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
    list_display = ('uid', 'title', 'hotel', 'uploaded')
    list_filter = ['hotel']


@admin.register(Room)
class RoomAdmin(ImportExportModelAdmin):
    list_display = ('name', 'hotel', 'price', 'author', 'created_at', 'updated_at')
    list_filter = ('hotel', 'author')
    search_fields = ['name']
    inlines = [ReservationInline]


@admin.register(Reservation)
class ReservationAdmin(ImportExportModelAdmin):
    list_display = ('room', 'start_date', 'end_date', 'author')
    list_filter = ('room', 'author')
    search_fields = ['room__name']
