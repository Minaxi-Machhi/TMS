from django.db.models import ForeignKey, ManyToManyField, OneToOneField

class BaseAdminMixin:
    """
    A base mixin for Django admin classes that automatically sets up `raw_id_fields`
    and some common admin options.

    Attributes:
        raw_id_fields (tuple): A tuple of field names that should use raw ID widgets.
        readonly_fields (tuple): A tuple of field names that are read-only in the admin.
        list_per_page (int): The number of items to display per page in the list view.
    """
    raw_id_fields = ()

    def __init__(self, model, admin_site, *args, **kwargs):
        """
        Initializes the mixin, setting up `raw_id_fields` and other common admin options.

        Args:
            model: The model class being registered with the admin.
            admin_site: The admin site instance.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        self.raw_id_fields = self.setup_raw_id_fields(model)
        self.readonly_fields = ('created', 'modified',)
        self.list_per_page = 10
        super().__init__(model, admin_site, *args, **kwargs)

    def setup_raw_id_fields(self, model):
        """
        Sets up `raw_id_fields` by identifying all ForeignKey, ManyToManyField,
        and OneToOneField fields in the model.

        Args:
            model: The model class being registered with the admin.

        Returns:
            list: A list of field names that should use raw ID widgets.
        """
        raw_id_fields = []
        for field in model._meta.get_fields():
            if any((isinstance(field, ForeignKey), isinstance(field, ManyToManyField),
                    isinstance(field, OneToOneField))):
                raw_id_fields.append(field.name)
        return raw_id_fields
