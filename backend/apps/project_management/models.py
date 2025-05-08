from django.contrib.auth.models import User
from django.db import models

from apps.core.models import UserProfile
from lib.base_models import BaseModel


# Create your models here.
class Project(BaseModel):
    code = models.CharField(max_length=100, unique=True, verbose_name='Project Code')
    name = models.CharField(max_length=255, verbose_name='Project Name')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_projects')

    def __str__(self):
        return self.name


class ProjectUser(BaseModel):
    project = models.ForeignKey(Project, related_name="project_users", on_delete=models.CASCADE)
    project_user = models.ForeignKey(UserProfile, related_name="project_user_projects", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.project.name} - {self.project_user}"
