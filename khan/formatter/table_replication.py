from .table import BaseTable


class ReplicationTable(BaseTable):
    __formatter_name__ = 'replication'

    def __init__(self, max_lines):
        header = {
            'Host': 15,
            'Port': 5,
            'State': 9,
            'Last Update': 19,
            'Delay': 7,
            'Health': 5,
            'Priority': 5,
            'Votes': 5,
            'Hidden': 5,
        }

        super(ReplicationTable, self).__init__(header, max_lines)
