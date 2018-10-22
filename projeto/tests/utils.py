#!/usr/bin/env python3
# encoding: utf-8

from decimal import Decimal
from contextlib import contextmanager

from rest_framework.test import APIClient

DEFAULT_PASSWORD = 'password'


def load_produtos(path):
    produtos = []
    with open(path, 'r') as fd:
        for line in fd.readlines():
            line = line.split(';')
            print('line', line)
            print('dado', line[0], line[1])
            produtos.append({
                'nome': line[0],
                'valor': Decimal(line[1]),
            })
    print('produtos', produtos)
    return produtos


class CustomAPIClient(APIClient):
    @contextmanager
    def auth(self, user=None, username=None, password=None,
             ignore_error=False):

        if password is None:
            password = DEFAULT_PASSWORD

        if username:
            success = self.login(username=username, password=password)
        elif user:
            success = self.login(username=user.username, password=password)
        else:
            raise Exception(
                'Please inform a username/password or a user object'
            )

        if not ignore_error and not success:
            raise Exception('Invalid user/password')

        yield self

        self.logout()
