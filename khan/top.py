import time
from operator import itemgetter
from prettytable import PrettyTable
from datetime import datetime as dt


class Top(object):

    def __init__(self, database_connection):
        self._database_connection = database_connection

    def start(self, repeat=60):
        start_time = time.time()

        for i in xrange(repeat):
            self._clear_shell()

            st = dt.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            print "### {} ###".format(st)
            self.current_status()

            time.sleep(1.0 - ((time.time() - start_time) % 1.0))

    def sort_operations_by(self, operations, field):
        for operation in operations:
            if field not in operation:
                operation[field] = 0

        return sorted(operations, key=itemgetter(field), reverse=True)

    def current_status(self):
        table = PrettyTable()
        table.field_names = [
            "#", "Id", "Op", "wfl",
            "Y", "Duration", "collection", "query"
        ]

        with self._database_connection.pymongo() as client:
            operations = client.current_op()['inprog']

        operations = self.sort_operations_by(operations, 'microsecs_running')
        for line, operation in enumerate(operations):

            query = "NULL"
            if "insert" in operation:
                query = str(operation["insert"])
            elif "query" in operation:
                query = str(operation["query"])

            duration = "NULL"
            if "microsecs_running" in operation:
                duration = str(operation.get("microsecs_running")/1000000) + "s"


            waitingForLock = 'Yes' if operation["waitingForLock"] else 'No'

            table.add_row([
                line, operation["connectionId"], operation["op"],
                waitingForLock, operation["numYields"], duration,
                operation["ns"], query[0:80]
            ])

            for i in xrange(80, len(query), 80):
                table.add_row(['', '', '', '', '', '', '', query[i:i+80]])

        print table

    def _clear_shell(self):
        print "\x1b[H\x1b[2J",
