from .table import BaseTable


class TopTable(BaseTable):
    __formatter_name__ = 'queries'

    def __init__(self, max_lines):
        header = {
            'Id': 8,
            'Op': 8,
            'wlf': 3,
            'Yields': 6,
            'Duration': 8,
            'collection': 25,
            'query': 75,
        }

        super(TopTable, self).__init__(header, max_lines)
