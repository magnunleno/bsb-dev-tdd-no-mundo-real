#!/usr/bin/env python3
# encoding: utf-8

from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


def test_valor_compra(client, fake_users, fake_produtos, fake_compras):
    '''
    Valida o valor total da compra, calculado com base no somatório de todos os
    produtos que compõem a compra.
    '''
    ...
