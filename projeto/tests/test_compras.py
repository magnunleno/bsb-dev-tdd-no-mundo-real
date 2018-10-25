#!/usr/bin/env python3
# encoding: utf-8

from datetime import datetime, date
from decimal import Decimal
from unittest.mock import patch
from django.urls import reverse
from django.utils.timezone import utc
from django.contrib.auth import get_user_model

from apps.pedidos import models
from tests.utils import dt_fmt

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
    url = reverse('compras-list')

    with client.auth(user=user):
        response = client.get(url)
        assert response.data == []
        assert models.Compra.objects.filter(comprador=user).count() == 0


def test_criar_compra(client, fake_users, fake_produtos):
    user = fake_users()
    produtos = fake_produtos(3)
    pks = [i.pk for i in produtos]
    url = reverse('compras-list')
    mock_data = datetime(2018, 1, 1, 15, 45).replace(tzinfo=utc)

    with client.auth(user=user):
        with patch('apps.pedidos.serializers.timezone.now') as mock:
            mock.return_value = mock_data
            response = client.post(url, {"produtos": pks}, format='json')

        assert response.status_code == 201
        assert models.Compra.objects.filter(comprador=user).count() == 1

        assert response.data['data_efetiva'] == dt_fmt(mock_data)
        assert response.data['data'] == dt_fmt(mock_data.date())
        assert response.data['pk'] is not None
        assert len(response.data['itens_compra']) == len(pks)

        produtos_armazenados = {}
        for item in response.data['itens_compra']:
            produtos_armazenados[item['pk_produto']] = {
                'nome': item['nome_produto'], 'valor': item['valor'],
            }

        for produto in produtos:
            armazenado = produtos_armazenados[produto.pk]
            assert armazenado['nome'] == produto.nome
            assert Decimal(armazenado['valor']) == produto.valor


def test_criar_compra_fds(client, fake_users, fake_produtos):
    user = fake_users()
    produtos = fake_produtos(3)
    pks = [i.pk for i in produtos]
    url = reverse('compras-list')
    mock_data = datetime(2018, 10, 13, 15, 45).replace(tzinfo=utc)

    with client.auth(user=user):
        with patch('apps.pedidos.serializers.timezone.now') as mock:
            mock.return_value = mock_data
            response = client.post(url, {"produtos": pks}, format='json')

        assert response.status_code == 201
        assert response.data['data_efetiva'] == dt_fmt(mock_data)
        assert response.data['data'] == dt_fmt(date(2018, 10, 15))


def test_segmentacao_compras_usuarios(client, fake_users, fake_produtos):
    users = fake_users(2)
    produtos = fake_produtos(2)
    pks = [i.pk for i in produtos]
    url = reverse('compras-list')

    with client.auth(user=users[0]):
        response = client.post(url, {"produtos": pks}, format='json')
        assert response.status_code == 201

        response = client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 1

    with client.auth(user=users[1]):
        response = client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 0


def test_compra_com_produto_inexistente(client, fake_users, fake_produtos):
    user = fake_users()
    pks = [1024, 1025]
    url = reverse('compras-list')

    with client.auth(user=user):
        response = client.post(url, {"produtos": pks}, format='json')
        assert response.status_code == 400
        assert response.data['produtos'][0] ==\
            'Não foi possível encontrar um ou mais produtos'

        response = client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 0
        assert models.Compra.objects.filter(comprador=user).count() == 0
