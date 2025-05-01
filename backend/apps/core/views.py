from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from apps.core import models, serializers
from lib.constants.base_constants import FieldConstants, Action
from lib.helpers import update_user_login_attempt
from lib.views import BaseViewSet


# Create your views here.
class LoginView(ObtainAuthToken):
    # throttle_classes = (UserLoginRateThrottle,)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})

        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data.get('user')

            if update_user_login_attempt(
                    user.username, FieldConstants.LOGIN_ATTEMPTS_CACHE_KEY_PREFIX
            ):
                return Response(
                    {"non_field_errors": ["Too many failed login attempts. Please try again later."]},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except ValidationError:
            username = request.data.get('username')
            if username and update_user_login_attempt(username, FieldConstants.LOGIN_ATTEMPTS_CACHE_KEY_PREFIX):
                return Response(
                    {"non_field_errors": ["Too many failed login attempts. Please try again later."]},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if user.user_profile and not user.user_profile.is_active:
            return Response(
                {"non_field_errors": ["User is not active."]},
                status=status.HTTP_400_BAD_REQUEST
            )

        update_user_login_attempt(
            user.username, FieldConstants.LOGIN_ATTEMPTS_CACHE_KEY_PREFIX, is_failed=False
        )

        token, created = Token.objects.get_or_create(user=user)
        # permissions = UserProfilePermissionSerializer(instance=user.user_profile).data
        # permissions = []

        response_data = {
            "token": token.key,
            "user_type": user.user_profile.user_type,
            # "detail": permissions,
            "profile_type": user.user_profile.user_type,
        }

        return Response(data=response_data, status=status.HTTP_200_OK)


class UserProfileViewSet(BaseViewSet):
    # filterset_class = UserProfileListFilter
    search_fields = (
        "user__first_name", "user__last_name", "user__username", "user__email", "contact_number",
        'user_role__role_name')
    model = models.UserProfile

    view_serializers = {
        Action.LIST: serializers.UserProfileSerializer,
        Action.RETRIEVE: serializers.UserProfileSerializer,
        Action.VIEW: serializers.UserProfileSerializer,
        Action.SELECT: serializers.UserProfileSerializer,

    }

    def get_queryset(self, *args, **kwargs):
        return UserProfile.objects.select_related("user_role").all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        roles = Role.objects.filter()
        context["all_roles"] = roles
        context["user"] = self.request.user
        context["default_branch"] = self.request.user.user_profile.default_branch
        return context


