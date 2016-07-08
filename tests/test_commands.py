# -*- coding: utf-8 -*-
import pytest
from khan import commands
from khan import mongodb_client
from . import factory


@pytest.fixture
def host():
    return 'pymongo.is.a.good.project.com'


@pytest.fixture
def port():
    return 27017


@pytest.fixture
def database():
    return 'admin'


@pytest.fixture
def database_fails():
    return 'admin_fails'


@pytest.fixture
def user():
    return 'user'


@pytest.fixture
def password():
    return 'password'


@pytest.fixture
def mongo_client(host, port, database, user, password):
    return mongodb_client.MongoDB(
        host, port, database, user, password, mongodb_client=factory.FakeMongoClient
    )


def test_factory_get_queries_command():
    assert commands.TopCommand == commands.command_factory('queries')


def test_factory_get_replication_command():
    assert commands.ReplicationCommand == commands.command_factory('replication')


def test_mongo_db_client_connection_string(mongo_client, user, password, host):
    connection_string = 'mongodb://{user}:{password}@{host}'.format(
        user=user, password=password, host=host
    )
    assert mongo_client._connection_string == connection_string


def test_database_client_init_databse_client(mongo_client, database):
    assert mongo_client._init_database_client()._name == database


def test_database_client_authenticate_succeds(mongo_client, user, password):
    auth_response = mongo_client._authenticate()
    assert auth_response['user'] == user
    assert auth_response['password'] == password


def test_database_client_fails_with_authentication_error(
    host, port, database_fails, user, password
):
    with pytest.raises(mongodb_client.AuthenticationError) as exc:
        mongodb_client.MongoDB(
            host, port, database_fails, user, password,
            mongodb_client=factory.FakeMongoClient
        )
    error_msg = 'Invalid credentials to database {}: mongodb://{}:{}@{}'.format(
        database_fails, user, password, host)
    assert str(exc.value) == error_msg
