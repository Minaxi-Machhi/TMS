from django.contrib import admin
from apps.project_management.models import Project, ProjectUser

# Register your models here.
admin.site.register(Project)
admin.site.register(ProjectUser)

