from django.contrib import admin
from apps.core.models import UserProfile, Role, ModulePermissions
from lib.mixin import BaseAdminMixin


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', "role", 'contact_number')
    search_fields = ('user__first_name', 'user__username', 'user__last_name', 'contact_number')
    list_filter = ('user_type', "role__role_name", 'created', 'modified')

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('role_name', 'is_system_generated',)
    search_fields = ('role_name',)
    list_filter = ('is_system_generated',)


@admin.register(ModulePermissions)
class ModulePermissionsAdmin(admin.ModelAdmin):
    list_display = ('module_name', 'name')
    search_fields = ('module_name',)


