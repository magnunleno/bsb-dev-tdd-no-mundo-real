#!/usr/bin/env python3
# encoding: utf-8

from datetime import date, timedelta


def get_dia_util(dia):
    if dia.weekday() <= 4:
        return dia

    delta = timedelta(days=(7 - dia.weekday()))
    return dia + delta
