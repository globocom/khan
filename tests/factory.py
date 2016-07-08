# -*- coding: utf-8 -*-
import pymongo


class FakeMongoClient(object):
    def __init__(self, connection_string, connectTimeoutMS):
        self._connection_string = connection_string
        self._connectTimeoutMS = connectTimeoutMS

    def __getattr__(self, name):
        return Database(name)


class Database(object):
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    def authenticate(self, user, password):
        if '_fails'in self._name:
            raise pymongo.errors.OperationFailure(Exception(), code=18)
        return {'user': user, 'password': password}

    def current_op(self, command):
        return {'it': 'works'}

    def command(self, command):
        return {'command': command}
