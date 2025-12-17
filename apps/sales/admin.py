from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'city', 'country')
    list_filter = ('country', 'created_at')
    search_fields = ('name', 'email', 'phone')
