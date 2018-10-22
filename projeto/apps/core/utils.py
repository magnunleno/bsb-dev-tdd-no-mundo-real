#!/usr/bin/env python3
# encoding: utf-8

from datetime import timedelta
from apps.core.models import Feriado


def e_dia_util(dia):
    query = Feriado.objects.filter(dia=dia)
    if query.exists():
        return False

    if dia.weekday() > 4:
        return False

    return True


def get_dia_util(dia):
    while True:
        if e_dia_util(dia):
            break
        dia = dia + timedelta(days=1)
    return dia
