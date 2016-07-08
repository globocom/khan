import time


class BaseCommand(object):

    def __init__(self, database_connection):
        self._database_connection = database_connection

    def start(self):
        start_time = time.time()

        while True:
            yield self._do()
            time.sleep(1.0 - ((time.time() - start_time) % 1.0))

    def _do(self):
        raise NotImplementedError()
