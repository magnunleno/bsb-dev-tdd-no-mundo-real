#!/usr/bin/env python3
# encoding: utf-8

from rest_framework import viewsets, permissions
from . import models, serializers


class ComprasViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.Compra
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return models.Compra.objects.filter(comprador=self.request.user)
