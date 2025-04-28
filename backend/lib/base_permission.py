class BasePermissions(object):
    TASK_MANAGEMENT = 'task_management'
    PROJECT_MANAGEMENT = 'project_management'
    USER_MANAGEMENT = 'user_management'

    ALL_PERMISSIONS = [
        TASK_MANAGEMENT,
        PROJECT_MANAGEMENT,
        USER_MANAGEMENT
    ]

    ADMIN_DEFAULT_PERMISSIONS = (
        TASK_MANAGEMENT,
        PROJECT_MANAGEMENT,
        USER_MANAGEMENT
    )

class PermissionConfig:
    permission_type_list = {
        'user_management': ['can_view', 'can_change'],
        'task_management': ['can_view', 'can_change'],
    }


