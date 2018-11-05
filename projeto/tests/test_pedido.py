#!/usr/bin/env python3
# encoding: utf-8

from decimal import Decimal
from datetime import datetime

from unittest.mock import patch
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.timezone import utc
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
        # Sem compras
        assert models.Compra.objects.filter(comprador=user).count() == 0
        response = client.get(url)
        assert response.data == []

        # Cria uma compra
        compra = fake_compras(comprador=user, produtos=fake_produtos(5))
        produto1 = compra.produtos.first()
        assert models.Compra.objects.filter(comprador=user).count() == 1

        # Valida listagem
        response = client.get(url)
        assert len(response.data) == 1
        c = response.data[0]
        assert int(c['pk']) == compra.pk
        assert c['data'] == dt_fmt(compra.data)
        assert c['data_efetiva'] == dt_fmt(compra.data_efetiva)
        assert len(c['itens_compra']) == 5
        assert int(c['itens_compra'][0]['produto_pk']) == produto1.pk
        assert c['itens_compra'][0]['produto_nome'] == produto1.nome
        assert Decimal(c['itens_compra'][0]['produto_valor']) == produto1.valor


def test_segmentacao_compras_usuarios(client, fake_users, fake_produtos,
                                      fake_compras):
    '''
    Somente o usuário que fez a compra deve visualizá-la.
    Ex: User_1 possui uma compra, porém User_2 não possui compras
    '''
    users = fake_users(2)
    url = reverse('compras-list')
    compra = fake_compras(comprador=users[0], produtos=fake_produtos(5))
    assert models.Compra.objects.count() == 1

    with client.auth(user=users[0]):
        response = client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 1
        assert int(response.data[0]['pk']) == compra.pk

    with client.auth(user=users[1]):
        response = client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 0


def test_criar_compra(client, fake_users, fake_produtos):
    '''
    Testa a criação de uma compra através da API, utilizando o patch de uma
    data.
    '''
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
        assert models.Compra.objects.filter(comprador=user).count() == 1
        compra = models.Compra.objects.first()
        ...
