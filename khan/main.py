# -*- coding: utf-8 -*-
import argparse
import json
from mongodb_client import MongoDB
from commands import command_factory
from formatter.table import show


def arg_parse():
    parser = argparse.ArgumentParser(
        add_help=True,
        description="Read the docs: https://github.com/globocom/khan"
    )

    parser.add_argument(
        '--host',
        help="MongoDB Host/instance",
        required=True
    )
    parser.add_argument(
        '--port',
        help="MongoDB port",
        required=True
    )
    parser.add_argument(
        '--database',
        help="Database name",
        required=True
    )
    parser.add_argument(
        "-u", dest='user',
        help="Database user",
        required=True
    )
    parser.add_argument(
        "-p", dest='password',
        help="Database password",
        required=True
    )
    parser.add_argument(
        "-m", dest='method',
        choices=[
            "queries",
            "replication"],
        help="Show <method> status",
        action="store"
    )
    parser.add_argument(
        "-f", dest='filters',
        help="Dictionary with key/column and value/contains. "
             "E.g: \"{'Op': 'query', 'collection': 'db.users'}\". "
             "Only to queries method",
        required=False, default={}
    )
    parser.add_argument(
        "-l", dest='max_lines', type=int,
        help="Max of lines in table",
        required=False, default=30
    )
    return parser.parse_args()


def main():
    parameters = arg_parse()

    connection = MongoDB(
        host=parameters.host, port=parameters.host,
        database=parameters.database, user=parameters.user,
        password=parameters.password
    )

    if parameters.filters:
        import ast
        parameters.filters = ast.literal_eval(parameters.filters)

    command_class = command_factory(parameters.method)
    command = command_class(connection, parameters.filters)

    for status in command.start():
        show(status, parameters.max_lines)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
