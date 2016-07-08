from operator import itemgetter
from collections import OrderedDict
from .base import BaseCommand


class TopCommand(BaseCommand):
    __command_name__ = 'queries'

    def _sort_operations_by(self, operations, field):
        return sorted(operations, key=itemgetter(field), reverse=True)

    def _is_waiting_for_lock(self, operation):
        return 'Yes' if operation["waitingForLock"] else 'No'

    def _get_duration_in_seconds(self, operation):
        return str(int(operation['microsecs_running'] / 1000000)) + "s"

    def _get_operations(self):
        operations = self._database_connection.current_op()['inprog']
        for operation in  operations:
            if 'microsecs_running' not in operation:
                operation['microsecs_running'] = 0
        return self._sort_operations_by(operations, 'microsecs_running')

    def _build_reponse_dict(self, operation, line, query):
        current = OrderedDict()
        current["Id"] = operation["connectionId"]
        current["Op"] = operation["op"]
        current["wfl"] = self._is_waiting_for_lock(operation)
        current["Yields"] = operation["numYields"]
        current["Duration"] = self._get_duration_in_seconds(operation)
        current["collection"] = operation["ns"]
        current["query"] = query
        return current

    def _do(self):
        result = []
        for line, operation in enumerate(self._get_operations()):
            query = "NULL"
            if "insert" in operation:
                query = str(operation["insert"])
            elif "query" in operation:
                query = str(operation["query"])

            current = self._build_reponse_dict(operation, line, query)
            if self.is_in_filter(current):
                result.append(current)

        return result

    def is_in_filter(self, values):
        if not self._filters:
            return True

        if not all(filter in values.keys() for filter in self._filters.keys()):
            raise AttributeError(
                "{} don't have {}".format(values.keys(), self._filters.keys())
            )

        return all(
            (self._filters[key] in values[key] for key in self._filters.keys())
        )
