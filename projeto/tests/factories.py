#!/usr/bin/env python3
# encoding: utf-8

from django.contrib.auth import get_user_model

import factory
import factory.fuzzy

from faker import Faker
from factory.django import DjangoModelFactory

from . import utils
from apps.pedidos.models import Produto

faker = Faker()
User = get_user_model()

PASSWORD = utils.DEFAULT_PASSWORD
PRODUTOS = utils.load_produtos('tests/data/produtos.txt')


class UserFactory(DjangoModelFactory):
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    password = factory.PostGenerationMethodCall('set_password', PASSWORD)

    @factory.lazy_attribute
    def username(self):
        return '{}_{}'.format(
            self.first_name.replace(' ', '_'),
            self.last_name.replace(' ', '_'),
        ).lower()

    @factory.lazy_attribute
    def email(self):
        return '{}.{}@example.com'.format(
            self.first_name.replace(' ', '_'),
            self.last_name.replace(' ', '_'),
        ).lower()

    class Meta:
        model = User


class ProdutosFactory(DjangoModelFactory):
    nome = factory.Iterator([i['nome'] for i in PRODUTOS])
    valor = factory.Iterator([i['valor'] for i in PRODUTOS])

    class Meta:
        model = Produto
