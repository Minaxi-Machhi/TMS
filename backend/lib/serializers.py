from django.contrib.auth import get_user_model
from rest_framework import serializers
# from rest_framework_gis.serializers import GeoModelSerializer

User = get_user_model()


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop("fields", None)
        exclude = kwargs.pop("exclude", None)

        # Adding this next line to the documented example
        read_only_fields = kwargs.pop("read_only_fields", None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        if exclude is not None:
            existing = set(self.fields)
            for field_name in existing:
                if field_name in exclude:
                    self.fields.pop(field_name)

        # another bit we're adding to documented example, to take care of readonly fields
        if read_only_fields is not None:
            for f in read_only_fields:
                try:
                    self.fields[f].read_only = True
                except KeyError:
                    # not in fields anyway
                    pass

    @staticmethod
    def validate_float_value(value):
        try:
            return float(value)
        except ValueError:
            raise serializers.ValidationError("A valid number is required.")


class ReadOnlyModelSerializer(DynamicFieldsModelSerializer):
    def get_fields(self):
        fields = super().get_fields()
        for field in fields.values():
            # set all field to read_only which eventually speed the response
            field.read_only = True
        return fields


class DateSerializer(serializers.DateField):
    def to_internal_value(self, data):
        if data:
            return super().to_internal_value(data)
        return None


class IntegerSerializer(serializers.IntegerField):
    default_value = 0

    def to_internal_value(self, data):
        if data:
            return super().to_internal_value(data)
        return self.default_value
