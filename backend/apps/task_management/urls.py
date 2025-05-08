from rest_framework.routers import DefaultRouter

from apps.task_management.views import TaskViewSet, BucketViewSet

task_router = DefaultRouter()
task_router.register('tasks', TaskViewSet, basename='task-list')
task_router.register('bucket', BucketViewSet, basename='bucket-list')
