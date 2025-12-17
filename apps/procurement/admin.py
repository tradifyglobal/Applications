from django.contrib import admin
from .models import Vendor


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'rating')
    list_filter = ('rating', 'created_at')
    search_fields = ('name', 'email', 'phone')
