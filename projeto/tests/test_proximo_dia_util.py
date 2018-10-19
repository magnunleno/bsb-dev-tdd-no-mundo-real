#!/usr/bin/env python3
# encoding: utf-8

import utils
from datetime import date


def test_dias_uteis():
    seg = date(2018, 10, 15)
    dia_util = utils.get_dia_util(seg)
    assert seg == dia_util

    ter = date(2018, 10, 16)
    dia_util = utils.get_dia_util(ter)
    assert ter == dia_util

    qua = date(2018, 10, 17)
    dia_util = utils.get_dia_util(qua)
    assert qua == dia_util

    qui = date(2018, 10, 18)
    dia_util = utils.get_dia_util(qui)
    assert qui == dia_util

    sex = date(2018, 10, 19)
    dia_util = utils.get_dia_util(sex)
    assert sex == dia_util

    sab = date(2018, 10, 20)
    dia_util = utils.get_dia_util(sab)
    assert sab != dia_util

    dom = date(2018, 10, 21)
    dia_util = utils.get_dia_util(dom)
    assert dom != dia_util


def test_dia_util_sab_dom():
    sab = date(2018, 10, 20)
    dia_util = utils.get_dia_util(sab)
    assert date(2018, 10, 22) == dia_util

    dom = date(2018, 10, 21)
    dia_util = utils.get_dia_util(dom)
    assert date(2018, 10, 22) == dia_util


def test_dia_util_sab_dom_virada_ano():
    sab = date(2018, 6, 30)
    dia_util = utils.get_dia_util(sab)
    assert date(2018, 7, 2) == dia_util
