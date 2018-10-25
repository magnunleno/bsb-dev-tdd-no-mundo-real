#!/usr/bin/env python3
# encoding: utf-8

from rest_framework import permissions
from drf_rw_serializers import viewsets
from . import models, serializers


class ComprasViewSet(viewsets.ModelViewSet):
    read_serializer_class = serializers.CompraReadOnlySerializer
    write_serializer_class = serializers.CompraSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return models.Compra.objects\
            .filter(comprador=self.request.user)\
            .select_related('comprador')\
            .prefetch_related('itens_compra', 'itens_compra__produto')
