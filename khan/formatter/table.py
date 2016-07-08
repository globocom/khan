from __future__ import print_function
from datetime import datetime as dt
import time
from prettytable import PrettyTable


MAX_COLUMN_LEN = 80
DATE_TIME_FORMAT = '%d-%m-%Y %H:%M:%S'


def show(lines):
    print(clear_shell(), end="")

    print(format_header())

    if not lines:
        print("Empty")
        return

    table = PrettyTable()
    table.field_names = lines[0].keys()

    for line in lines:
        column = 0
        while True:
            values = []
            for info in line.values():
                values.append(format_column(info, column))

            if not any(values):
                break

            table.add_row(values)
            column += MAX_COLUMN_LEN

    print(table)


def format_column(info, column):
    if isinstance(info, dt):
        info = info.strftime(DATE_TIME_FORMAT)

    return str(info)[column:column + MAX_COLUMN_LEN]


def format_header():
    st = dt.fromtimestamp(time.time()).strftime(DATE_TIME_FORMAT)
    return "### {} ###".format(st)


def clear_shell():
    return "\x1b[H\x1b[2J"
