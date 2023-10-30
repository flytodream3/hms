from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from .models import HotelUser, Profile


class HotelUserCreationForm(UserCreationForm):
    class Meta:
        model = HotelUser
        fields = ('is_customer',)


class HotelUserChangeForm(UserChangeForm):
    class Meta:
        model = HotelUser
        fields = ('password', 'first_name', 'last_name', 'email', 'is_manager', 'is_customer', 'is_staff', 'is_owner')


@admin.register(HotelUser)
class HotelUserAdmin(UserAdmin):
    list_display = (
        'username', 'first_name', 'last_name', 'phone', 'email', 'is_manager', 'is_customer'
    )
    list_filter = ('is_manager', 'is_customer')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal', {'fields': ('email', 'first_name', 'last_name', 'phone')}),
        ('Permissions',
         {'fields': (
             'is_active', 'is_staff', 'is_superuser', 'is_customer',
             'is_manager', 'is_owner', 'groups', 'user_permissions'
         )
          }
         ),
        ('Info', {'fields': ('date_joined', 'last_login')})
    )
    ordering = ('username', 'email', 'first_name', 'last_name')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'dob', 'address', 'city', 'state', 'country')
    list_filter = ['state', 'city']
    search_fields = ['user__username', 'address']