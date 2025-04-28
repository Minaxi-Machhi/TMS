from django.contrib import admin

# Register your models here.
from django.contrib import admin
from apps.task_management.models import Task

admin.site.register(Task)
