from __future__ import print_function
from datetime import datetime as dt
import time
from prettytable import PrettyTable


DATE_TIME_FORMAT = '%d-%m-%Y %H:%M:%S'
FIELD_SIZE = {
    'Host': 15,
    'Port': 5,
    'State': 9,
    'Last Update': 19,
    'Delay': 7,
    'Health': 5,
    'Priority': 5,
    'Votes': 5,
    'Hidden': 5,
    'Id': 8,
    'Op': 8,
    'wlf': 3,
    'Yields': 6,
    'Duration': 8,
    'collection': 25,
    'query': 80,
}


def show(lines):
    print(clear_shell(), end="")

    print(format_header())

    if not lines:
        print("Empty")
        return

    table = PrettyTable()
    table.field_names = lines[0].keys()
    table.align = "l"

    for line in lines:
        table_line = 0
        while True:
            values = []
            for key in line.keys():
                values.append(format_column(key, line[key], table_line))

            if not any(values):
                break

            table.add_row(values)
            table_line += 1

    print(table)


def format_column(key, info, table_line):
    if isinstance(info, dt):
        info = info.strftime(DATE_TIME_FORMAT)
    info = str(info)

    if key in FIELD_SIZE:
        diff = FIELD_SIZE[key] - len(info)
        if diff > 0:
            info += ' ' * diff

        current_size = FIELD_SIZE[key] * table_line
        return str(info)[current_size:current_size + FIELD_SIZE[key]]

    return ''


def format_header():
    st = dt.fromtimestamp(time.time()).strftime(DATE_TIME_FORMAT)
    return "### {} ###".format(st)


def clear_shell():
    return "\x1b[H\x1b[2J"
