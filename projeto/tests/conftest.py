#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from . import factories, utils


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture(scope='function')
def client():
    return utils.CustomAPIClient()


@pytest.fixture(scope='function')
def fake_users(db):
    def make_fake_users(count=1, is_staff=False):
        if count == 1:
            return factories.UserFactory(is_staff=is_staff)
        else:
            return factories.UserFactory.create_batch(count, is_staff=is_staff)
    return make_fake_users
