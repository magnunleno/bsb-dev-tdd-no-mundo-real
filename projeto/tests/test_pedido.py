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
    url = reverse('compras-list')

    response = client.get(url)
    assert response.status_code == 403

    user = fake_users()
    with client.auth(user=user):
        response = client.get(url)
    assert response.status_code == 200
