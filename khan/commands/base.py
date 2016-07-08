import time


class BaseCommand(object):
    __command_name__ = ''

    def __init__(self, database_connection, command_options, filters=None):
        self._filters = filters
        self._database_connection = database_connection
        self._refresh = command_options['refresh']

    def start(self):
        start_time = time.time()

        while True:
            yield self._do()
            time.sleep(self._refresh - ((time.time() - start_time) % 1.0))

    def _do(self):
        raise NotImplementedError()
