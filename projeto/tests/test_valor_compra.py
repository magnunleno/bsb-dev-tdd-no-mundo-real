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
    user = fake_users()
    compra = fake_compras(comprador=user, produtos=fake_produtos(3))
    valor_total = sum([produto.valor for produto in compra.produtos.all()])
    url = reverse('compras-detail', args=[compra.pk])

    with client.auth(user=user):
        response = client.get(url)
        assert response.status_code == 200
        assert response.data['valor_total'] == valor_total
