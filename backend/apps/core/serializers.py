from django.utils import timezone
from rest_framework import serializers
from rest_framework.authtoken.admin import User

from apps.core.models import UserProfile
from lib.base_permission import BasePermissions
from lib.constants.base_constants import UserProfileConstants
from lib.helpers import encrypt
from lib.serializers import DynamicFieldsModelSerializer


class UserSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class UserProfileSerializer(DynamicFieldsModelSerializer):
    permissions = serializers.SerializerMethodField(read_only=True)
    username = serializers.CharField(required=True, )
    first_name = serializers.CharField(required=True, )
    last_name = serializers.CharField(required=True, )
    email = serializers.CharField(required=True, )
    password = serializers.CharField(
        required=False, write_only=True, allow_null=True)

    class Meta:
        model = UserProfile
        fields = (
            'id', 'contact_number', 'is_active', 'user_type', 'permissions', 'username',
            'first_name', 'last_name', 'email', 'password', 'phone_code')
        read_only_fields = ('id', 'user', 'created', 'updated')

    @staticmethod
    def get_permissions(instance):
        base_permissions = None
        if instance.user_type == [UserProfileConstants.SYSTEM_ADMIN, UserProfileConstants.MANAGER, UserProfileConstants.TEAM_MEMBER]:
            base_permissions = BasePermissions.ADMIN_DEFAULT_PERMISSIONS
        all_perms = {}
        if base_permissions:
            role_permissions = instance.user_type.permissions.filter(
                name__in=base_permissions)

            for permission in base_permissions:
                all_perms[permission] = {'change': False, 'view': False}

            for perm in role_permissions:
                action, module = perm.permission_type, perm.name
                if action in all_perms[module]:
                    all_perms[module][action] = True

        return all_perms

    def validate(self, attrs):
        is_active = attrs.get("is_active", False)
        # user = self.context.get('user', None)

        if not self.instance:
            self.validate_create(attrs)
        else:
            self.validate_update(attrs)

        attrs['is_active'] = is_active

        attrs['user_type'] = attrs.get("user_type", None)
        return attrs

    def validate_update(self, attrs):
        username = attrs.pop("username", self.instance.user.username)
        first_name = attrs.pop("first_name", self.instance.user.first_name)
        last_name = attrs.pop("last_name", self.instance.user.last_name)
        email = attrs.pop("email", self.instance.user.email)
        attrs["user_details"] = {
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
        }

        user_serializer = UserSerializer(instance=self.instance.user, data=attrs["user_details"],
                                         context=self.context, partial=True)
        user_serializer.is_valid(raise_exception=True)

        attrs['user'] = user_serializer

    def validate_create(self, attrs):
        username = attrs.pop("username")
        first_name = attrs.pop("first_name")
        last_name = attrs.pop("last_name", None)
        email = attrs.pop("email", None)
        password = attrs.pop("password", None)
        if password is None:
            raise serializers.ValidationError(
                {'Password': "Password is required!"})
       
        attrs["user_details"] = {
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,
        }
        user_serializer = UserSerializer(
            data=attrs['user_details'], context=self.context)
        user_serializer.is_valid(raise_exception=True)
        return attrs

    def create(self, validated_data):
        user_details = validated_data.pop("user_details", None)
        if user_details:
            validated_data["user"] = User.objects.create_user(**user_details)
            validated_data.pop('password', None)
            user_profile = super(UserProfileSerializer, self).create(validated_data)
            user_profile.save()
            return user_profile

    #
    # def update(self, instance, validated_data):
    #     updated_password = validated_data.pop("password", None)
    #     branches = validated_data.pop("branches", [])
    #     user_details = validated_data.pop("user", None)
    #     update_profile = validated_data.pop("update_profile", None)
    #
    #     if updated_password:
    #         validate_new_password(updated_password)
    #
    #         recent_passwords_list = instance.recent_passwords.split(',') if instance.recent_passwords else []
    #
    #         for password in recent_passwords_list:
    #             if decrypt(password.encode('utf-8')) == updated_password:
    #                 raise serializers.ValidationError({"non_field_errors": [
    #                     "This password has been used previously. Please choose a different password."]})
    #
    #         instance.user.set_password(updated_password)
    #         validated_data['password_updated_at'] = timezone.now()
    #
    #         recent_passwords_list.append(encrypt(updated_password).decode('utf-8'))
    #         if len(recent_passwords_list) > 4:
    #             recent_passwords_list.pop(0)
    #         instance.recent_passwords = ','.join(recent_passwords_list)
    #
    #     if user_details:
    #         user_details.save()
    #
    #     user_profile = super(UserProfileSerializer, self).update(instance, validated_data)
    #
    #     new_branches_object = []
    #     if branches and instance.branches.exists():
    #         previous_branches = set(instance.branches.values_list("id", flat=True))
    #         branches = set(branches)
    #         new_branches = branches.difference(previous_branches)
    #         for branch in new_branches:
    #             new_branches_object.append(BranchUser(user_profile=instance, branch=branch))
    #
    #         deleted_branches = previous_branches.difference(branches)
    #         if deleted_branches:
    #             BranchUser.objects.filter(branch__in=deleted_branches, user_profile=instance).delete()
    #     else:
    #         for branch in branches:
    #             new_branches_object.append(BranchUser(user_profile=instance, branch=branch))
    #
    #     if new_branches_object:
    #         BranchUser.objects.bulk_create(new_branches_object)
    #         instance.default_branch = new_branches_object[0].branch
    #
    #     try:
    #         if not update_profile:
    #             instance.user.auth_token.delete()
    #     except User.auth_token.RelatedObjectDoesNotExist as e:
    #         logger.exception(e)
    #     except TypeError as te:
    #         logger.exception(te)
    #
    #     return user_profile
    #
