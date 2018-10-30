#!/usr/bin/env python3
# encoding: utf-8

from datetime import timedelta


def get_dia_util(dia):
    if dia.weekday() == 5:
        return dia + timedelta(days=2)
    if dia.weekday() == 6:
        return dia + timedelta(days=1)
    return dia
