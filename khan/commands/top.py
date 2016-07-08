from operator import itemgetter
from collections import OrderedDict
from .base import BaseCommand


class TopCommand(BaseCommand):
    __command_name__ = 'queries'

    def sort_operations_by(self, operations, field):
        for operation in operations:
            if field not in operation:
                operation[field] = 0

        return sorted(operations, key=itemgetter(field), reverse=True)

    def _do(self):
        result = []
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
                duration = str(operation.get("microsecs_running") / 1000000) + "s"

            waitingForLock = 'Yes' if operation["waitingForLock"] else 'No'

            current = OrderedDict()
            current["#"] = line
            current["Id"] = operation["connectionId"]
            current["Op"] = operation["op"]
            current["wfl"] = waitingForLock
            current["Yields"] = operation["numYields"]
            current["Duration"] = duration
            current["collection"] = operation["ns"]
            current["query"] = query

            if self.is_in_filter(current):
                result.append(current)

        return result

    def is_in_filter(self, values):
        if not self._filters:
            return True

        if self._filters.keys() not in values.keys():
            raise AttributeError(
                "{} don't have {}".format(values.keys(), self._filters.keys())
            )

        return all((self._filters[key] in values[key] for key in self._filters.keys()))
