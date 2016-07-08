from __future__ import print_function
from dateutil import tz
from collections import OrderedDict
from .base import BaseCommand


class ReplicationCommand(BaseCommand):
    __command_name__ = 'replication'

    def _do(self):
        result = []

        replSetGetStatus = self._database_connection.execute_command('replSetGetStatus')
        replSetGetConfig = self._database_connection.execute_command('replSetGetConfig')

        config_members = {}
        for member in replSetGetConfig['config']['members']:
            config_members[member['host']] = member

        optimeDate_Primary = None
        for member in replSetGetStatus['members']:
            if member['stateStr'] == 'PRIMARY':
                optimeDate_Primary = member['optimeDate'].replace(tzinfo=tz.tzutc()).astimezone(tz.tzlocal())

        for member in replSetGetStatus['members']:
            name = member['name']
            host, port = name.split(":")
            state = member['stateStr']
            if member.get('health', 1) == 1:
                health = 'Up'
            else:
                health = 'Down'

            delay = '-'
            optimeDate = '-'
            if state != 'ARBITER':
                optimeDate = member['optimeDate'].replace(tzinfo=tz.tzutc()).astimezone(tz.tzlocal())
                if optimeDate_Primary:
                    delay = optimeDate_Primary - optimeDate

            priority = config_members[name]['priority']
            votes = config_members[name]['votes']
            hidden = config_members[name]['hidden']

            current = OrderedDict()
            current["Host"] = host
            current["Port"] = port
            current["State"] = state
            current["Last Update"] = optimeDate
            current["Delay"] = delay
            current["Health"] = health
            current["Priority"] = priority
            current["Votes"] = votes
            current["Hidden"] = hidden
            result.append(current)

        return result
