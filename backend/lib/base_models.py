import contextlib

from django.contrib.gis.db import models as gis_models
from django.db import models
from django.db.models import ForeignObjectRel, ManyToManyRel, OneToOneRel, BooleanField, CharField
from model_utils.models import TimeStampedModel


class BaseModel(TimeStampedModel):
    ORDERING = ("-modified", "-created")
    created_by = models.CharField(verbose_name="Created By", max_length=100, blank=True, null=True)
    updated_by = models.CharField(verbose_name="Updated By", max_length=100, blank=True, null=True)

    class Meta:
        abstract = True

    @property
    def added_on(self):
        return self.created

    @property
    def updated_on(self):
        return self.modified

    def save(self, *args, **kwargs):
        if self.pk:
            # If self.pk is not None then it's an update.
            cls = self.__class__
            old = cls.objects.get(pk=self.pk)
            # This will get the current model state since super().save() isn't called yet.
            new = self  # This gets the newly instantiated Mode object with the new values.
            changed_fields = []
            for field in cls._meta.get_fields():
                field_name = field.name
                with contextlib.suppress(Exception):
                    if getattr(old, field_name) != getattr(new, field_name):
                        changed_fields.append(field_name)
            kwargs['update_fields'] = changed_fields
        super().save(*args, **kwargs)

    @classmethod
    def get_raw_id_fields(cls) -> object:
        return [
            field.name
            for field in cls._meta.get_fields()
            if any(
                (
                    isinstance(field.remote_field, ForeignObjectRel),
                    isinstance(field.remote_field, ManyToManyRel),
                    isinstance(field.remote_field, OneToOneRel),
                )
            )
        ]

    @classmethod
    def get_list_filter_fields(cls, *args):
        list_filter = ["created", "modified"]
        exclude_fields = iter(args)
        list_filter.extend(
            field.name
            for field in cls._meta.get_fields()
            if (
                    isinstance(field.remote_field, ForeignObjectRel)
                    and field.name == "branch"
            )
            or (
                    (
                            isinstance(field, BooleanField)
                            or (isinstance(field, CharField) and field.choices)
                    )
                    and field.name not in exclude_fields
            )
        )

        return list_filter
