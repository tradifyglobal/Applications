from django.contrib import admin
from .models import Equipment, MaintenanceRequest


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'location')
    list_filter = ('location',)
    search_fields = ('code', 'name')


@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ('ticket_no', 'equipment', 'status', 'priority', 'created_at')
    list_filter = ('status', 'priority', 'created_at')
    search_fields = ('ticket_no',)
