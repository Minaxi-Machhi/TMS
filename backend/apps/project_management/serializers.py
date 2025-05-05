from apps.core.serializers import UserSerializer
from apps.project_management.models import Project
from apps.task_management.serializers import TaskSerializer
from lib.serializers import DynamicFieldsModelSerializer


class ProjectSerializer(DynamicFieldsModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'tasks', 'created_at', 'code']
