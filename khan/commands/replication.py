from __future__ import print_function
from prettytable import PrettyTable
from dateutil import tz
from .base import BaseCommand


class ReplicationCommand(BaseCommand):

    def _do(self):
        table = PrettyTable()
        table.field_names = [
            "Host", "Port", "State", "Last Update", "Delay", "Health",
            "Priority", "Votes", "Hidden",
        ]

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

            if state == 'ARBITER':
                delay = '-'
                optimeDate_str = '-'
            else:
                optimeDate = member['optimeDate'].replace(tzinfo=tz.tzutc()).astimezone(tz.tzlocal())
                optimeDate_str = optimeDate.strftime('%d-%m-%Y %H:%M:%S')
                if optimeDate_Primary:
                    delay = optimeDate_Primary - optimeDate
                else:
                    delay = '-'

            priority = config_members[name]['priority']
            votes = config_members[name]['votes']
            hidden = config_members[name]['hidden']

            table.add_row([host, port, state, optimeDate_str, delay, health,
                          priority, votes, hidden])

        print(table)
