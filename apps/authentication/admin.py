from django.contrib import admin
from .models import Group, User


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_date')
    list_filter = ('is_active',)
    search_fields = ('name',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'status', 'is_staff', 'last_login')
    list_filter = ('status', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'first_name')
