import logging

from apps.core.pagination import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from . import constants, mixins
from .constants.base_constants import Action, Method
from .helpers import get_response_message

logger = logging.getLogger(__name__)


class BaseGenericViewSet(mixins.ViewSetMixin, viewsets.GenericViewSet):
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)

    model = None
    filterset_class = None

    class Meta:
        abstract = True

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user"] = self.request.user
        return context

    @action(methods=[constants.Method.GET], detail=False)
    def choices(self, queryset, *args, **kwargs):
        response = BaseViewSet.get_choices_for_model_fields(self.model)
        return Response(data=response, status=status.HTTP_200_OK)


class BaseViewSet(mixins.ViewSetMixin, viewsets.ModelViewSet):
    filter_backends = (filters.SearchFilter, OrderingFilter, DjangoFilterBackend)

    model = None
    pagination_class = CustomPagination
    filterset_class = None
    view_serializers = {}

    http_method_names = [
        Method.GET,
        Method.HEAD,
        Method.OPTIONS,
        Method.POST,
        Method.PATCH,
        Method.PUT,
        Method.DELETE,
    ]
    def get_serializer_class(self):
        serializer_dict = self.view_serializers

        if not serializer_dict:
            return self.serializer_class

        request_action = self.action
        if request_action == Action.LIST:
            return serializer_dict[request_action]
        return serializer_dict[constants.Action.RETRIEVE]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user"] = self.request.user
        context["request"] = self.request
        return context

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response_data = serializer.data

        if not isinstance(request.data, list):
            response = {
                "response_data": response_data,
                "message": get_response_message(response_data, self.model, self.action)
            }
        else:
            response = response_data
        return Response(data=response, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        response_data = serializer.data
        action_name = "update" if partial else self.action
        response = {
            "response_data": response_data,
            "message": get_response_message(response_data, self.model, action_name)
        }
        return Response(data=response, status=status.HTTP_200_OK)

    @action(methods=[constants.Method.GET], detail=True)
    def view(self, queryset, *args, **kwargs):
        obj = self.get_object()
        serializer = self.view_serializers[self.action](obj, context={"request": self.request})
        return Response(serializer.data)

    @action(methods=[constants.Method.GET], detail=False)
    def select(self, queryset, *args, **kwargs):
        queryset = self.get_queryset()
        filtered_queryset = self.filter_queryset(queryset=queryset)
        paginated_queryset = self.paginate_queryset(filtered_queryset)
        if paginated_queryset is not None:
            serializer = self.view_serializers[self.action](paginated_queryset, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(self.view_serializers[self.action](filtered_queryset, many=True).data)
