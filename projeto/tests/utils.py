#!/usr/bin/env python3
# encoding: utf-8

from decimal import Decimal
from contextlib import contextmanager
from datetime import datetime, date

from rest_framework.test import APIClient

DEFAULT_PASSWORD = 'password'


def load_produtos(path):
    produtos = []
    with open(path, 'r') as fd:
        for line in fd.readlines():
            line = line.split(';')
            produtos.append({
                'nome': line[0],
                'valor': Decimal(line[1]),
            })
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


def dt_fmt(dt):
    if not dt:
        return dt

    if type(dt) == datetime:
        return dt.isoformat().split('+')[0] + 'Z'
    else:
        return dt.strftime('%Y-%m-%d')
