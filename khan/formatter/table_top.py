from collections import OrderedDict
from .table import BaseTable


class TopTable(BaseTable):
    __formatter_name__ = 'queries'

    def __init__(self, max_lines):
        header = OrderedDict()
        header['Id'] = 8
        header['Op'] = 8
        header['wfl'] = 3
        header['Yields'] = 6
        header['Duration'] = 8
        header['collection'] = 25
        header['query'] = 75

        super(TopTable, self).__init__(header, max_lines)
