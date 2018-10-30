#!/usr/bin/env python3
# encoding: utf-8

from datetime import date
from apps.core import utils


def test_dias_uteis():
    '''
    Testa se a função get_dia_util retorna a mesma data para dias úteis e datas
    diferentes para fins de semana
    '''
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
    '''
    Valida que, ao informar sab ou dom, a data retornada será segunda.
    '''
    sab = date(2018, 10, 20)
    dia_util = utils.get_dia_util(sab)
    assert date(2018, 10, 22) == dia_util

    dom = date(2018, 10, 21)
    dia_util = utils.get_dia_util(dom)
    assert date(2018, 10, 22) == dia_util


def test_dia_util_sab_dom_virada_mes():
    '''
    Valida que, ao informar uma data em que há virada de mês no fim de semana,
    a data retornada está correta.
    Ex: 2018-06-30 => 2018-07-02
    '''
    sab = date(2018, 6, 30)
    dia_util = utils.get_dia_util(sab)
    assert date(2018, 7, 2) == dia_util
