from django_filters import rest_framework

from apps.core.models import UserProfile


class UserFilters(rest_framework.FilterSet):
    class Meta:
        model = UserProfile
        fields = ["user_type"]
