from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.models import UserProfile
from apps.project_management import models, serializers
from apps.project_management.models import ProjectUser
from lib.constants.base_constants import Action, UserProfileConstants, Method
from lib.views import BaseViewSet


# Create your views here.
class ProjectViewSet(BaseViewSet):
    model = models.Project
    search_fields = ('search_string',)

    view_serializers = {
        Action.LIST: serializers.ProjectSerializer,
        Action.RETRIEVE: serializers.ProjectSerializer,
        Action.VIEW: serializers.ProjectSerializer,
    }

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()

        if user.user_profile.user_type == UserProfileConstants.SYSTEM_ADMIN:
            return queryset
        elif user.user_profile.company.company_type == UserProfileConstants.TEAM_MEMBER:
            return queryset.filter(collaborators=user).distinct()
        elif user.user_profile.company.company_type == UserProfileConstants.MANAGER:
            return queryset
        return queryset

    def get_serializer_context(self):
        context = super(ProjectViewSet, self).get_serializer_context()
        context["request"] = self.request
        return context

    @action(methods=[Method.POST], detail=True)
    def add_user(self, request, *args, **kwargs):
        project = self.get_object()
        user_ids = request.data.get("user_ids")

        if not user_ids:
            return Response({"error": "users is required"}, status=status.HTTP_400_BAD_REQUEST)

        users = UserProfile.objects.filter(id__in=user_ids)
        for user in users:
            if ProjectUser.objects.filter(project=project, project_user=user).exists():
                return Response({"message": "User already added to project"}, status=status.HTTP_200_OK)

            ProjectUser.objects.create(project=project, project_user=user)
        return Response({"message": "Users added to project"}, status=status.HTTP_201_CREATED)
