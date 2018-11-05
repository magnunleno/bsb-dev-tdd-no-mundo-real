#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import date

import pytest
from . import factories, utils
from apps.core.utils import get_dia_util
from apps.pedidos.models import Compra, ItemCompra


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture(scope='function')
def client():
    return utils.CustomAPIClient()


@pytest.fixture(scope='function')
def fake_users(db):
    def make_fake_users(count=1, is_staff=False):
        if count == 1:
            return factories.UserFactory(is_staff=is_staff)
        else:
            return factories.UserFactory.create_batch(count, is_staff=is_staff)
    return make_fake_users


@pytest.fixture(scope='function')
def fake_produtos(db):
    def make_fake_produto(count=1, *args, **kwargs):
        if count == 1:
            return factories.ProdutosFactory(*args, **kwargs)
        else:
            return factories.ProdutosFactory.create_batch(
                count, *args, **kwargs
            )
    return make_fake_produto


@pytest.fixture(scope='function')
def fake_compras(db):
    def make_fake_compra(comprador, produtos):
        compra = Compra.objects.create(
            data=get_dia_util(date.today()),
            comprador=comprador,
        )
        itens = [ItemCompra(produto=p, compra=compra, valor=p.valor)
                 for p in produtos]
        ItemCompra.objects.bulk_create(itens)
        return compra
    return make_fake_compra
