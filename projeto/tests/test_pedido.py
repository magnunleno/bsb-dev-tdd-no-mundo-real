#!/usr/bin/env python3
# encoding: utf-8

from decimal import Decimal

from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.pedidos import models
from tests.utils import dt_fmt

User = get_user_model()


def test_compras_exige_login(client, fake_users):
    '''
    Valida que a URL de realizar uma compra só pode ser acessada por usuários
    logados.
    '''
    url = reverse('compras-list')

    response = client.get(url)
    assert response.status_code == 403

    user = fake_users()
    with client.auth(user=user):
        response = client.get(url)
    assert response.status_code == 200


def test_compras_vazias(client, fake_users, fake_produtos, fake_compras):
    '''
    Valida a listagem de compras existentes
    '''
    user = fake_users()
    url = reverse('compras-list')

    with client.auth(user=user):
        ...
