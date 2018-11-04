#!/usr/bin/env python3
# encoding: utf-8

from datetime import timedelta
from apps.core.models import Feriado


def eh_feriado(dia):
    queryset = Feriado.objects.filter(dia=dia)
    if queryset.exists():
        return True

    if dia.weekday() in (5, 6):
        return True
    return False


def get_dia_util(dia):
    while True:
        if not eh_feriado(dia):
            break
        dia += timedelta(days=1)
    return dia
