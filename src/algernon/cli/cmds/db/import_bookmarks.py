import argparse
from typing import Any

from backinajiffy.mama.rc import Rc

from algernon.cli.utils import AlgnBaseCmd, import_bookmarks

CMD = __name__.split('.')[-1].replace('_', '-')


def add_subcommand(sps: argparse._SubParsersAction):
    p = sps.add_parser(CMD, help='Import bookmarks from a JSON list')
    p.add_argument(
        'fn',
        help='JSON file'
    )
    p.set_defaults(cmd=DbImportBookmarksCmd)


class DbImportBookmarksCmd(AlgnBaseCmd):

    async def get_result(self) -> Any:
        rc = Rc.get_instance()
        fn = rc.g('fn')
        return await import_bookmarks(fn, self.DbSessionMaker, self.login)
