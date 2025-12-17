from django.contrib import admin
from .models import Site


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('site_code', 'site_name', 'city', 'country', 'is_active')
    list_filter = ('is_active', 'country')
    search_fields = ('site_code', 'site_name', 'city')
