from django.shortcuts import render

from apps.task_management import models, serializers
from apps.task_management.serializers import  TaskSerializer
from lib.constants.base_constants import Action
from lib.views import BaseViewSet

class BucketViewSet(BaseViewSet):
    model = models.Bucket
    view_serializers = {
        Action.LIST: serializers.BucketSerializer,
        Action.CREATE: serializers.BucketSerializer,
        Action.RETRIEVE: serializers.BucketSerializer,
        Action.VIEW: serializers.BucketSerializer,
        Action.SELECT: serializers.BucketSerializer,
    }
    # filterset_class = BucketFilters

class TaskViewSet(BaseViewSet):
    model = models.Task
    serializer_class = TaskSerializer
