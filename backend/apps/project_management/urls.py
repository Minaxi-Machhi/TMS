from rest_framework.routers import DefaultRouter

from apps.project_management.views import ProjectViewSet

project_router = DefaultRouter()
project_router.register('projects', ProjectViewSet, basename='project-list')