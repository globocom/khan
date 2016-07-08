import sys
import inspect
from .replication import ReplicationCommand
from .top import TopCommand


def command_factory(command_name):
    klasses = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    for klass in klasses:
        if klass[1].__command_name__ == command_name:
            return klass[1]
    else:
        raise AttributeError('Unknown method: {}'.format(command_name))
