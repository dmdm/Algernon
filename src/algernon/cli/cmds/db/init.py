import argparse
from pathlib import Path
from typing import Any

from backinajiffy.mama.rc import Rc

from algernon.cli.utils import AlgnBaseCmd
from algernon.common.db.utils import init_db

CMD = __name__.split('.')[-1].replace('_', '-')


def add_subcommand(sps: argparse._SubParsersAction):
    p = sps.add_parser(CMD, help='Initializes the database, i.e. creates tables etc. '
                                 'The database and its owner must already exist.')
    p.add_argument(
        '--drop',
        action='store_true',
        help='Drop tables etc before creating them?'
    )
    p.set_defaults(cmd=DbInitCmd)


class DbInitCmd(AlgnBaseCmd):

    async def get_result(self) -> Any:
        rc = Rc.get_instance()
        drop = rc.g('drop')

        fn_alembic_ini = Path(__file__).parent.parent.parent.parent.parent.parent / 'alembic.ini'
        await init_db(engine=self.dbengine, DbSession=self.DbSession, fn_alembic_ini=fn_alembic_ini, drop=drop)
        return True
