from django.contrib.auth.models import User
from django.db import models

from apps.project_management.models import Project
from lib.base_models import BaseModel
from lib.constants import base_constants


# Create your models here.
class Task(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=base_constants.TaskConstants.get_status_choices(), default=base_constants.TaskConstants.TO_DO)
    priority = models.CharField(max_length=15, choices=base_constants.TaskConstants.get_priority_choices(), default=base_constants.TaskConstants.MEDIUM)
    # labels = models.ManyToManyField('Label', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title