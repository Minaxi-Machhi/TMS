from django.shortcuts import render

from apps.project_management import models, serializers
from lib.constants.base_constants import Action, UserProfileConstants
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