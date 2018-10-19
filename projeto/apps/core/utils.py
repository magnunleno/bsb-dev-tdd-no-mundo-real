#!/usr/bin/env python3
# encoding: utf-8

from datetime import timedelta
from apps.core.models import Feriado


def get_dia_util(dia):
    query = Feriado.objects.filter(dia=dia)
    if query.exists():
        return dia + timedelta(days=1)

    if dia.weekday() <= 4:
        return dia

    delta = timedelta(days=(7 - dia.weekday()))
    return dia + delta
