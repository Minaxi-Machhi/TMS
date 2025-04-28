class Method:
    GET = "get"
    HEAD = "head"
    OPTIONS = "options"
    POST = "post"
    PUT = "put"
    PATCH = "patch"
    DELETE = "delete"


class Action:
    CREATE = "create"
    DESTROY = "destroy"
    LIST = "list"
    PARTIAL_UPDATE = "partial_update"
    RETRIEVE = "retrieve"
    UPDATE = "update"
    VIEW = "view"
    SELECT = "select"
    BULK_CREATE = "bulk_create"
    EXPORT = "export"


class FieldConstants:
    PHONE_NUMBER_LENGTH = 12
    PHONE_CODE_LENGTH = 5
    DEFAULT_PHONE_CODE = "966"
    ADDRESS_LENGTH = 200
    NAME_LENGTH = 200
    DATE_TIME_FORMATS = ("%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S",
                         "%Y-%m-%dT%H:%M:%S")
    DATE_FORMAT = "%Y-%m-%d"
    TIME_FORMAT = "%H:%M"
    MULTIPLE_DATE_FORMATS = ("%m/%d/%Y", "%m-%d-%Y",
                             "%d-%m-%Y", "%d/%m/%Y", "%Y-%m-%d", "%Y/%m/%d")
    DATE_TIME_FORMAT = "%Y-%m-%d %H:%M"
    VOLUMETRIC_WEIGHT_CONSTANT = 5000


class FileFieldConstants:
    FILE_SIZE = 5 * 1024 * 1024
    IMAGE_FORMATS = ['png', 'jpg', 'jpeg']
    DOCUMENT_FORMATS = ['doc', 'docx', 'pdf', 'xlsx', 'xls']
    VIDEO_FORMATS = ["mp4", "mkv", 'wmv', 'mov', "avi", "webm"]
    AUDIO_FORMATS = ['mp3', 'aac', 'wav']
    IMAGE_PDF_FORMATS = IMAGE_FORMATS + ['pdf']
    IMAGE_PDF_DOC_FORMATS = IMAGE_FORMATS + ['pdf', 'doc', 'docx', ]
    ATTACHMENT_FORMATS = IMAGE_FORMATS + DOCUMENT_FORMATS + AUDIO_FORMATS


class SystemRoles:
    SYS_ADMIN = "System Administrator"
    ADMIN = "Admin"
    MANAGER = "Manager"
    TEAM_MEMBER = "Team Member"

class TaskConstants:
    TO_DO, IN_PROGRESS, CODE_REVIEW, COMPLETED = ['To Do', 'In Progress', 'Code Review', 'Completed']
    LOW, MEDIUM, HIGH = ['Low', 'Medium', 'High']

    @classmethod
    def get_status_choices(cls):
        return [(cls.TO_DO, 'To Do'), (cls.IN_PROGRESS, 'In Progress'), (cls.CODE_REVIEW, 'Code Review'), (cls.COMPLETED, 'Completed')]

    @classmethod
    def get_priority_choices(cls):
        return [(cls.LOW, 'Low'), (cls.MEDIUM, 'Medium'), (cls.HIGH, 'High')]

class UserProfileConstants:
    USER_PROFILE_HISTORY_EXCLUDE_FIELDS = ["updated_by", "created_by", 'default_branch', 'created', 'modified']
    ROLE_HISTORY_EXCLUDE_FIELDS = ["updated_by", "created_by", 'created', 'modified']
    USER_HISTORY_INCLUDE_FIELDS = ["username", "first_name", "last_name", "email", "password", ]
    MANAGER, SYSTEM_ADMIN, TEAM_MEMBER = ('Manager', 'System Admin', 'Team Member')
    MANAGER, SYSTEM_ADMIN, TEAM_MEMBER = ('Manager', 'System Admin', 'Team Member')

    @classmethod
    def get_user_type_choices(cls):
        return ((cls.MANAGER, 'Manager'),
                (cls.TEAM_MEMBER, 'Team Member'),
                (cls.SYSTEM_ADMIN, 'System Admin'))

    @classmethod
    def get_profile_type_choices(cls):
        PROFILE_TYPE_CHOICES = ((cls.SYSTEM_ADMIN, 'System Admin'),
                                (cls.TEAM_MEMBER, 'Team Member'),
                                (cls.MANAGER, 'Manager'))
        return PROFILE_TYPE_CHOICES
