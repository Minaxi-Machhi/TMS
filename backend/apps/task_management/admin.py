from django.contrib import admin

# Register your models here.
from django.contrib import admin
from apps.task_management.models import Task, Bucket, TaskAssignment


@admin.register(Bucket)
class BucketAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'due_date', 'status', 'bucket', 'priority')
    search_fields = ('title','project', 'due_date', 'status', 'bucket', 'priority')


@admin.register(TaskAssignment)
class TaskAssignmentAdmin(admin.ModelAdmin):
    list_display = ('task', 'user')
    search_fields = ('task', 'user')
