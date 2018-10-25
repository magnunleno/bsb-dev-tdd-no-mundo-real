#!/usr/bin/env python3
# encoding: utf-8

from unittest.mock import patch
from django.urls import reverse
from django.utils.timezone import utc
from django.contrib.auth import get_user_model

User = get_user_model()


def test_valor_compra(client, fake_users, fake_produtos):
    user = fake_users()
    produtos = fake_produtos(10)
    valor_total = sum([produto.valor for produto in produtos[:3]])
    pks = [i.pk for i in produtos[:3]]
    url = reverse('compras-list')

    with client.auth(user=user):
        response = client.post(url, {"produtos": pks}, format='json')
        assert response.status_code == 201
        assert response.data['valor_total'] == valor_total


def test_valor_compra_apos_alteracao_produto(client, fake_users, fake_produtos):
    user = fake_users()
    produtos = fake_produtos(10)
    valor_total = sum([produto.valor for produto in produtos[:3]])
    pks = [i.pk for i in produtos[:3]]
    url = reverse('compras-list')

    with client.auth(user=user):
        response = client.post(url, {"produtos": pks}, format='json')
        assert response.status_code == 201
        compra_pk = response.data['pk']

        url = reverse('compras-detail', args=[compra_pk])

        response = client.get(url)
        assert response.status_code == 200
        assert response.data['valor_total'] == valor_total

        produtos[0].valor += 5
        produtos[0].save()

        response = client.get(url)
        assert response.status_code == 200
        assert response.data['valor_total'] == valor_total
