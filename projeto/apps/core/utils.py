#!/usr/bin/env python3
# encoding: utf-8

from datetime import timedelta
from apps.core.models import Feriado


def get_dia_util(dia):
    queryset = Feriado.objects.filter(dia=dia)
    if queryset.exists():
        return dia + timedelta(days=1)

    if dia.weekday() == 5:
        return dia + timedelta(days=2)
    if dia.weekday() == 6:
        return dia + timedelta(days=1)
    return dia
