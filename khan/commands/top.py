from __future__ import print_function
from operator import itemgetter
from prettytable import PrettyTable
from .base import BaseCommand


class TopCommand(BaseCommand):

    def sort_operations_by(self, operations, field):
        for operation in operations:
            if field not in operation:
                operation[field] = 0

        return sorted(operations, key=itemgetter(field), reverse=True)

    def _do(self):
        table = PrettyTable()
        table.field_names = [
            "#", "Id", "Op", "wfl",
            "Yields", "Duration", "collection", "query"
        ]

        operations = self._database_connection.current_op()['inprog']
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

        print(table)
