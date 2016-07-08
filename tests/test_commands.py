# -*- coding: utf-8 -*-
from khan import commands


def test_factory_get_queries_command():
    assert commands.TopCommand == commands.command_factory('queries')


def test_factory_get_replication_command():
    assert commands.ReplicationCommand == commands.command_factory('replication')
