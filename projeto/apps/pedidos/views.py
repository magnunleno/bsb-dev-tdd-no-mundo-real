#!/usr/bin/env python3
# encoding: utf-8

from rest_framework import viewsets, permissions
from rest_framework.response import Response


class ComprasViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request):
        return Response([])

    def create(self, request):
        return Response([])
