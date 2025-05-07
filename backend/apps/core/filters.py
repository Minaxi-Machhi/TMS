from django_filters import rest_framework as filters, CharFilter
from apps.core.models import UserProfile
from apps.project_management.models import ProjectUser


class UserFilters(filters.FilterSet):
    project = filters.CharFilter(method='project_users')

    def project_users(self, queryset, name, value):
        user_ids = ProjectUser.objects.filter(project=value).values_list('project_user__id', flat=True)
        return queryset.exclude(id__in=user_ids)

    class Meta:
        model = UserProfile
        fields = ["user_type", "project"]
