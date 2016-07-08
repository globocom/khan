# -*- coding: utf-8 -*-
import pytest
from khan import mongodb_client
from . import factory


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


def test_database_client_current_op_succeds(mongo_client):
    response = mongo_client.current_op()
    assert response == {'it': 'works'}


def test_database_client_execute_command_succeds(mongo_client):
    command_name = "myCommand"
    response = mongo_client.execute_command(command_name)
    assert response == {'command': command_name}
