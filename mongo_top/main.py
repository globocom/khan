# -*- coding: utf-8 -*-
import argparse

def arg_parse():
    parser = argparse.ArgumentParser(
        add_help=True,
        description="Read the docs: https://github.com/globocom/mongo-top"
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
    return parser.parse_args()


def main():
    parameters = arg_parse()
    print parameters.host
    print parameters.port
    print parameters.database
    print parameters.user
    print parameters.password
    print parameters.is_query


if __name__ == '__main__':
    main()