from apps.core.serializers import UserSerializer
from apps.project_management.models import Project
from apps.task_management.serializers import TaskSerializer
from lib.serializers import DynamicFieldsModelSerializer


class ProjectSerializer(DynamicFieldsModelSerializer):
    owner = UserSerializer(read_only=True)
    collaborators = UserSerializer(many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner', 'collaborators', 'tasks', 'created_at', 'code']
