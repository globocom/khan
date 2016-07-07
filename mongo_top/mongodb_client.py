# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from contextlib import contextmanager
import logging
import pymongo

LOG = logging.getLogger(__name__)

MONGO_CONNECTION_DEFAULT_TIMEOUT = 5


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

    @property
    def _connection_string(self):
        return 'mongodb://{user}:{password}@{host}'.format(
            user=self._user, password=self._password, host=self._host)

    def _init_database_client(self):
        client = getattr(pymongo.MongoClient(
            self._connection_string,
            connectTimeoutMS=self._timeout
        ), self._database)

        client.authenticate(self._user, self._password)
        return client


    @contextmanager
    def pymongo(self):
        client = None
        try:
            yield self._init_database_client()
        except pymongo.errors.OperationFailure, e:
            if e.code == 18:
                error_message = 'Invalid credentials to database {}: {}'.format(
                    self._name, self._connection_string)
                raise AuthenticationError(error_message)
        except pymongo.errors.PyMongoError, e:
            error_message = 'Error connecting to database {}: {}'.format(
                self._name, self._connection_string)
            raise ConnectionError(error_message)
        finally:
            try:
                if client:
                    client.close()
            except Exception:
                pass
