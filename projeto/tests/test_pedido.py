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
    ...
