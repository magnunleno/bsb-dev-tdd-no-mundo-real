#!/usr/bin/env python3
# encoding: utf-8

from rest_framework import permissions
from rest_framework.response import Response
from drf_rw_serializers.viewsets import (CreateModelMixin, ListModelMixin,
                                         RetrieveModelMixin, GenericViewSet)

from . import models, serializers


class ComprasViewSet(CreateModelMixin, ListModelMixin, RetrieveModelMixin,
                     GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.CompraSerializer
    read_serializer_class = serializers.CompraReadOnlySerializer

    def get_queryset(self):
        return models.Compra.objects.filter(comprador=self.request.user)
