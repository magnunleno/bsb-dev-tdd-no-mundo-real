#!/usr/bin/env python3
# encoding: utf-8

from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


def test_compras_exige_login(client, fake_users):
    '''
    Valida que a URL de realizar uma compra só pode ser acessada por usuários
    logados.
    '''
    ...
