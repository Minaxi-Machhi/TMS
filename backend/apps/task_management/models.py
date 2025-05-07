from django.contrib.auth.models import User
from django.db import models

from apps.project_management.models import Project
from lib.base_models import BaseModel
from lib.constants import base_constants


# Create your models here.
class Bucket(BaseModel):
    name = models.CharField(max_length=100, null=True, blank=True, default='To do')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Task(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assignees = models.ManyToManyField(User, through='TaskAssignment', related_name='task_assignments')
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=base_constants.TaskConstants.get_status_choices(), default=base_constants.TaskConstants.TO_DO)
    priority = models.CharField(max_length=15, choices=base_constants.TaskConstants.get_priority_choices(), default=base_constants.TaskConstants.MEDIUM)
    bucket = models.ForeignKey(Bucket, related_name='tasks', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class TaskAssignment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
