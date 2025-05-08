import logging

from django.contrib.postgres.fields.array import ArrayField
from django.db.models import CharField
from django.utils.encoding import force_str
from rest_framework import status
from rest_framework.decorators import action
# from rest_framework.response import Response

from lib import helpers, constants
from lib.helpers import get_user_full_name

# from lib.constants import UserProfileConstants
# from lib.helpers import get_bulk_upload_response_message
# from lib.helpers import get_data_based_on_branch, get_user_full_name

logger = logging.getLogger(__name__)


class ViewSetMixin:
    def get_queryset(self):
        queryset = self.model.objects.all().order_by('-created')
        # user_type = self.request.user.user_profile.user_type
        # if user_type == CompanyConstants.CUSTOMER and helpers.is_field_in_model(self.model, "customer"):
        #     return queryset.filter(customer=self.request.user.user_profile.company)
        # if self.request.user.user_profile.profile_type in [UserProfileConstants.FINANCE,
        #                                                    UserProfileConstants.SYSTEM_ADMIN]:
        #     return queryset
        # if user_type in [UserProfileConstants.NORMAL, UserProfileConstants.REGIONAL]:
        #     model_name = self.model._meta.model_name
        #     return get_data_based_on_branch(self, queryset, branch=None, model_name=model_name)

        return queryset

    @property
    def is_added_by_required(self):
        return helpers.is_field_in_model(self.model, "added_by")

    @property
    def is_created_by_required(self):
        return helpers.is_field_in_model(self.model, "created_by")

    @property
    def get_default_create_parameters(self):
        user = self.request.user
        save_parameters = {"created_by": user.username}

        if self.is_added_by_required:
            save_parameters["added_by"] = user

        if self.is_created_by_required:
            full_name = get_user_full_name(
                self)
            save_parameters["created_by"] = full_name

        return save_parameters

    def perform_create(self, serializer):
        save_parameters = self.get_default_create_parameters
        serializer.save(**save_parameters)

    def perform_update(self, serializer):
        full_name = get_user_full_name(self)
        serializer.save(updated_by=full_name)

    @classmethod
    def get_choices_for_model_fields(cls, model):
        parsed_choices = {}
        for field in model._meta.get_fields():
            if isinstance(field, CharField) and field.choices or isinstance(field, ArrayField):
                field_choices = field.choices
                if isinstance(field, ArrayField) and isinstance(field.base_field, CharField):
                    field_choices = field.base_field.choices
                parsed_choices[field.name] = [
                    {
                        'value': choice_value,
                        'display_name': force_str(choice_name, strings_only=True)
                    }
                    for choice_value, choice_name in dict(field_choices).items()
                ]
        return parsed_choices


# class BulkUploadModelMixin:
#     """
#     Bulk upload for a model
#     """
#
#     @action(methods=[constants.Method.POST], detail=False)
#     def bulk_create(self, request, *args, **kwargs):
#         context = self.get_serializer_context()
#         data = request.data
#         serializer = self.view_serializers[constants.Action.BULK](data=data, many=True, context=context,
#                                                                   )
#         if not serializer.is_valid(raise_exception=True):
#             raise serializer.errors
#         else:
#             added_by = request.user
#             full_name = get_user_full_name(self)
#             serializer.save(created_by=full_name, added_by=added_by)
#         response = {
#             "message": get_bulk_upload_response_message(self.model)
#         }
#         return Response(response, status=status.HTTP_200_OK)
