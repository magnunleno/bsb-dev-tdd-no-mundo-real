#!/usr/bin/env python3
# encoding: utf-8

from datetime import date


def get_dia_util(dia):
    if dia.weekday() == 5:
        return date(dia.year, dia.month, dia.day + 2)
    if dia.weekday() == 6:
        return date(dia.year, dia.month, dia.day + 1)
    return dia
