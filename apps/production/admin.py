from django.contrib import admin
from .models import WorkOrder


@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ('work_order_no', 'status', 'start_date', 'end_date')
    list_filter = ('status', 'start_date')
    search_fields = ('work_order_no',)
