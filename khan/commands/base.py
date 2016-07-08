from __future__ import print_function
import time
from datetime import datetime as dt


class BaseCommand(object):

    def __init__(self, database_connection):
        self._database_connection = database_connection

    def start(self):
        start_time = time.time()

        while True:
            self._clear_shell()

            st = dt.fromtimestamp(time.time()).strftime(
                '%Y-%m-%d %H:%M:%S')
            print("### {} ###".format(st))
            self._do()

            time.sleep(1.0 - ((time.time() - start_time) % 1.0))

    def _do(self):
        raise NotImplementedError()

    def _clear_shell(self):
        print("\x1b[H\x1b[2J", end="")
