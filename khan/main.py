# -*- coding: utf-8 -*-
import argparse
from mongodb_client import MongoDB
from commands import command_factory
from formatter import formatter_factory


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
        "-r", dest='refresh',
        help="Refresh (seconds)",
        default=1,
        type=int,
        required=False
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

    command_options = {
        'refresh': parameters.refresh,
    }

    if parameters.filters:
        import ast
        parameters.filters = ast.literal_eval(parameters.filters)

    command_class = command_factory(parameters.method)
    command = command_class(connection, command_options, parameters.filters)

    table_class = formatter_factory(parameters.method)
    table = table_class(parameters.max_lines)

    for status in command.start():
        table.show(status)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
