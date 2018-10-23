#!/usr/bin/env python3
# encoding: utf-8

from django.urls import reverse
from django.contrib.auth import get_user_model

from apps.pedidos import models

User = get_user_model()


def test_compras_exige_login(client, fake_users):
    url = reverse('compras-list')

    response = client.get(url)
    assert response.status_code == 403

    user = fake_users()
    with client.auth(user=user):
        response = client.get(url)
        assert response.status_code == 200


def test_compras_vazias(client, fake_users, fake_produtos):
    user = fake_users()
    produtos = fake_produtos(3)
    url = reverse('compras-list')

    with client.auth(user=user):
        response = client.get(url)
        assert response.data == []
        assert models.Compra.objects.filter(comprador=user).count() == 0

        response = client.post(url, {
            "produtos": [produtos[0].pk]
        })
        assert response.status_code == 201
        assert models.Compra.objects.filter(comprador=user).count() == 1
