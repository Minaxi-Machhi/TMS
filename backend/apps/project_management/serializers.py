from rest_framework import serializers

from apps.core.serializers import UserSerializer, UserProfileSerializer
from apps.project_management.models import Project
from apps.task_management.serializers import TaskSerializer
from lib.serializers import DynamicFieldsModelSerializer


class ProjectSerializer(DynamicFieldsModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    project_users = serializers.SerializerMethodField(read_only=True)
    owner_name = serializers.CharField(source='owner.username')

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'tasks', 'created_at', 'code', 'owner_name', 'project_users']

    def create(self, validated_data):
        request = self.context.get("request", None)
        validated_data['owner'] = request.user if request else None
        return super(ProjectSerializer, self).create(validated_data)

    def get_project_users(self, obj):
        project_users = obj.project_users.select_related('project_user')
        return UserProfileSerializer([pu.project_user for pu in project_users], many=True).data