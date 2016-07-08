import sys
import inspect
from .table_top import TopTable
from .table_replication import ReplicationTable

def formatter_factory(command_name):
    klasses = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    for klass in klasses:
        if klass[1].__formatter_name__ == command_name:
            return klass[1]
    else:
        raise AttributeError('Unknown method: {}'.format(command_name))
