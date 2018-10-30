#!/usr/bin/env python3
# encoding: utf-8

from datetime import timedelta


def get_dia_util(dia):
    if dia.weekday() > 4:
        return None
    return dia
