from __future__ import print_function
from datetime import datetime as dt
import time
from prettytable import PrettyTable


DATE_TIME_FORMAT = '%d-%m-%Y %H:%M:%S'


class BaseTable(object):
    def __init__(self, header, max_lines=30):
        self.header = header
        self.max_lines = max_lines

    def show(self, lines):
        print(self.clear_shell(), end="")

        print(self.format_header())

        table = PrettyTable()
        table.field_names = self.header.keys()
        table.align = "l"

        for line in lines:
            table_line = 0
            while True:
                values = []
                for key in line.keys():
                    values.append(self.format_column(key, line[key], table_line))

                if not any(values):
                    break

                table.add_row(values)
                table_line += 1

            if len(table._rows) >= self.max_lines:
                break

        print(table)


    def format_column(self, key, info, table_line):
        if isinstance(info, dt):
            info = info.strftime(DATE_TIME_FORMAT)
        info = str(info)

        if key in self.header:
            diff = self.header[key] - len(info)
            if diff > 0:
                info += ' ' * diff

            current_size = self.header[key] * table_line
            return str(info)[current_size:current_size + self.header[key]]

        return ''


    def format_header(self):
        st = dt.fromtimestamp(time.time()).strftime(DATE_TIME_FORMAT)
        return "### {} ###".format(st)


    def clear_shell(self):
        return "\x1b[H\x1b[2J"
