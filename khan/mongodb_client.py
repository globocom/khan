# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from contextlib import contextmanager
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
                 user, password, timeout=MONGO_CONNECTION_DEFAULT_TIMEOUT):
        self._host = host
        self._port = port
        self._database = database
        self._user = user
        self._password = password
        self._timeout = timeout
        self._client = self._init_database_client()

        try:
            self._authenticate()
        except pymongo.errors.OperationFailure as e:
            if e.code == 18:
                error_message = 'Invalid credentials to database {}: {}'.format(
                    self._database, self._connection_string)
                raise AuthenticationError(error_message)

    @property
    def _connection_string(self):
        return 'mongodb://{user}:{password}@{host}'.format(
            user=self._user, password=self._password, host=self._host)

    def _init_database_client(self):
        client = getattr(pymongo.MongoClient(
            self._connection_string,
            connectTimeoutMS=self._timeout
        ), self._database)

        return client

    def _authenticate(self):
        return self._client.authenticate(self._user, self._password)

    @contextmanager
    def pymongo(self):
        try:
            yield self._client
        except pymongo.errors.PyMongoError as e:
            error_message = 'Error connecting to database {}: {}\n{}'.format(
                self._database, self._connection_string, e)
            raise ConnectionError(error_message)
