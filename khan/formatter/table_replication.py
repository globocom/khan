from collections import OrderedDict
from .table import BaseTable


class ReplicationTable(BaseTable):
    __formatter_name__ = 'replication'

    def __init__(self, max_lines):
        header = OrderedDict()
        header['Host'] = 15
        header['Port'] = 5
        header['State'] = 9
        header['Last Update'] = 19
        header['Delay'] = 7
        header['Health'] = 5
        header['Priority'] = 5
        header['Votes'] = 5
        header['Hidden'] = 5

        super(ReplicationTable, self).__init__(header, max_lines)
