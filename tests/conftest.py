# -*- coding: utf-8 -*-
import pytest
from khan import mongodb_client
from . import factory


@pytest.fixture(scope="module")
def host():
    return 'pymongo.is.a.good.project.com'


@pytest.fixture(scope="module")
def port():
    return 27017


@pytest.fixture(scope="module")
def database():
    return 'admin'


@pytest.fixture(scope="module")
def database_fails():
    return 'admin_fails'


@pytest.fixture(scope="module")
def user():
    return 'user'


@pytest.fixture(scope="module")
def password():
    return 'password'


@pytest.fixture(scope="module")
def mongo_client(host, port, database, user, password):
    return mongodb_client.MongoDB(
        host, port, database, user, password, mongodb_client=factory.FakeMongoClient
    )
