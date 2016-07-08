# -*- coding: utf-8 -*-
import argparse
from mongodb_client import MongoDB
from commands.replication import ReplicationCommand
from commands.top import TopCommand


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
        "-u",  dest='user',
        help="Database user",
        required=True
    )
    parser.add_argument(
        "-p", dest='password',
        help="Database password",
        required=True
    )
    parser.add_argument(
        "-q", dest='is_query',
        help="Show current queries",
        action="store_true"
    )
    parser.add_argument(
        "-r", dest='is_replication',
        help="Show replication status",
        action="store_true"
    )
    return parser.parse_args()


def main():
    parameters = arg_parse()

    connection = MongoDB(
        host=parameters.host, port=parameters.host,
        database=parameters.database, user=parameters.user,
        password=parameters.password
    )

    if parameters.is_query:
        TopCommand(connection).start()

    if parameters.is_replication:
        ReplicationCommand(connection).start()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
