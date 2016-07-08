# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import logging
import pymongo

LOG = logging.getLogger(__name__)

MONGO_CONNECTION_DEFAULT_TIMEOUT = 5000


class AuthenticationError(Exception):
    pass


class ConnectionError(Exception):
    pass


class MongoDB(object):
    def __init__(self, host, port, database,
                 user, password, timeout=MONGO_CONNECTION_DEFAULT_TIMEOUT,
                 mongodb_client=pymongo.MongoClient):
        self._host = host
        self._port = port
        self._database = database
        self._user = user
        self._password = password
        self._timeout = timeout
        self._mongodb_client = mongodb_client
        self._authenticate()

    @property
    def _connection_string(self):
        return 'mongodb://{user}:{password}@{host}'.format(
            user=self._user, password=self._password, host=self._host)

    def _init_database_client(self):
        client = getattr(self._mongodb_client(
            self._connection_string,
            connectTimeoutMS=self._timeout

        ), self._database)

        return client

    def _authenticate(self):
        self._client = self._init_database_client()
        try:
            return self._client.authenticate(self._user, self._password)
        except pymongo.errors.OperationFailure as e:
            if e.code == 18:
                error_message = 'Invalid credentials to database {}: {}'.format(
                    self._database, self._connection_string)
                raise AuthenticationError(error_message)

    def _execute(self, func, attempts=10, command=None):
        try:
            return func(command)
        except pymongo.errors.PyMongoError as e:
            if attempts > 0:
                print('Reconnecting... Attemps: {}'.format(attempts))
                self._authenticate()
                return self._execute(func, attempts - 1, command)
            else:
                error_message = 'Error connecting to database {}: {}\n{}'.format(
                    self._database, self._connection_string, e)
                raise ConnectionError(error_message)

    def current_op(self):
        return self._execute(self._client.current_op)

    def execute_command(self, command):
        return self._execute(self._client.command, command=command)
