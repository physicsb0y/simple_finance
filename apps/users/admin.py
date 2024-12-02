from django.contrib import admin

from .models import User

# Register your models here.

@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'phone_numbers', 'date_of_birth', 'citizenship_number', 'address']
    search_fields = ['email', 'first_name', 'last_name', 'phone_numbers', 'date_of_birth', 'citizenship_number', 'address']
    list_filter = ['email', 'first_name', 'last_name', 'phone_numbers', 'date_of_birth']
    ordering = ['email', 'first_name', 'last_name', 'phone_numbers']
