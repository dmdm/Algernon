import argparse
import sys

from backinajiffy.mama.cli import import_subcommands

CMD = __name__.split('.')[-1].replace('_', '-')


def add_subcommand(sps: argparse._SubParsersAction):
    p = sps.add_parser(CMD, help='Perform actions on users')
    import_subcommands(p, sys.modules[__name__])
