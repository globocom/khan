import time
from operator import itemgetter
from prettytable import PrettyTable
from datetime import datetime as dt
from dateutil import tz


class Replication(object):

    def __init__(self, database_connection):
        self._database_connection = database_connection

    def status(self, repeat=1):
        start_time = time.time()

        for i in xrange(repeat):
            self._clear_shell()

            st = dt.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            print "### {} ###".format(st)
            self.current_status()

            time.sleep(1.0 - ((time.time() - start_time) % 1.0))

    def current_status(self):
        table = PrettyTable()
        table.field_names = [
            "Host", "Port", "State", "Last Update", "Delay", "Health"
        ]

        with self._database_connection.pymongo() as client:
            replSetGetStatus = client.command('replSetGetStatus')
            replSetGetConfig = client.command('replSetGetConfig')

        optimeDate_Primary = None
        for member in replSetGetStatus['members']:
            if member['stateStr'] == 'PRIMARY':
                optimeDate_Primary = member['optimeDate'].replace(tzinfo=tz.tzutc()).astimezone(tz.tzlocal())

        for member in replSetGetStatus['members']:
            host, port = member['name'].split(":")
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

            table.add_row([host, port, state, optimeDate_str, delay, health])

        print table

    def _clear_shell(self):
        print "\x1b[H\x1b[2J",
