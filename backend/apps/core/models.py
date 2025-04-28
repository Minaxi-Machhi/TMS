from django.contrib.auth.models import User
from django.db import models

from lib.base_models import BaseModel
from lib.constants import base_constants


class ModulePermissions(BaseModel):
    name = models.CharField('Permission name', max_length=255)
    module_name = models.CharField('Module name', max_length=255)

    class Meta:
        verbose_name = 'Module Permission'
        verbose_name_plural = "Module Permissions"

    def __str__(self) -> str:
        return f'Can {self.module_name} {self.name} '


class Role(BaseModel):
    role_name = models.CharField(max_length=50, verbose_name='Role name')
    is_system_generated = models.BooleanField(default=False)
    module_permissions = models.ManyToManyField(
        ModulePermissions, verbose_name='Module Permissions', blank=True,
        help_text='Specific permissions for this role.',
        related_name="roles", related_query_name="module_roles")
    profile_type = models.CharField(max_length=20,
                                    choices=base_constants.UserProfileConstants.get_profile_type_choices(),
                                    blank=True, null=True, default=base_constants.UserProfileConstants.SYSTEM_ADMIN,
                                    verbose_name='Profile Type')

    class Meta:
        ordering = BaseModel.ORDERING
        verbose_name_plural = "Roles"

    def __str__(self) -> str:
        return f'{self.role_name}'

class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    contact_number = models.CharField(max_length=15,
                                      verbose_name="User Contact Number", blank=True, null=True, unique=True,
                                      error_messages={'unique': "User with this contact number already exists."})
    phone_code = models.CharField(max_length=base_constants.FieldConstants.PHONE_CODE_LENGTH,
                                  default=base_constants.FieldConstants.DEFAULT_PHONE_CODE,
                                  verbose_name="Contact Number Country Code", null=True, blank=True)
    user_type = models.CharField(max_length=12, choices=base_constants.UserProfileConstants.get_user_type_choices(),
                                 default=base_constants.UserProfileConstants.SYSTEM_ADMIN, verbose_name='User Type')
    is_active = models.BooleanField(default=True, verbose_name='Is Active')
    role = models.ForeignKey(Role, related_name="role_users", on_delete=models.SET_NULL,
                             verbose_name="User Role", null=True, blank=True)

    class Meta:
        ordering = BaseModel.ORDERING
        verbose_name_plural = "User Profiles"
