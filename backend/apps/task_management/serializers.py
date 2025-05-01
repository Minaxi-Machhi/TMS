from rest_framework import serializers

from apps.core.serializers import UserSerializer
from apps.task_management.models import Task
from lib.serializers import DynamicFieldsModelSerializer


class TaskSerializer(DynamicFieldsModelSerializer):
    project = serializers.StringRelatedField()
    assigned_to = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'project', 'assigned_to', 'due_date',
                  'priority', 'status', 'created_at', 'updated_at']
