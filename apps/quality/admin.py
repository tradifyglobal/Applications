from django.contrib import admin
from .models import QualityCheck


@admin.register(QualityCheck)
class QualityCheckAdmin(admin.ModelAdmin):
    list_display = ('check_date', 'status', 'created_at')
    list_filter = ('status', 'check_date')
