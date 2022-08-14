import argparse
import logging
from typing import Optional, Tuple

from sqlalchemy import orm

from backinajiffy.mama import cli
from backinajiffy.mama.exc import MamaError
from backinajiffy.mama.rc import Rc

from algernon.common.db.utils import create_engines, create_session


class AlgnBaseCmd(cli.BaseCmd):

    def __init__(self,
                 args: argparse.Namespace,
                 cmd_name: Optional[str] = None,
                 lgg: Optional[logging.Logger] = None,
                 catch: Optional[Tuple] = (MamaError,),
                 exit_code_error: Optional[int] = 1,
                 finally_cb=None):
        super().__init__(args=args, cmd_name=cmd_name, lgg=lgg, catch=catch, exit_code_error=exit_code_error,
                         finally_cb=finally_cb)
        rc = Rc.get_instance()
        self.dsn = rc.g('dsn')
        self.echo_sql = rc.g('echo_sql')
        self.login = rc.g('login')
        self.login_pwd = rc.g('login_pwd')
        self.dbengine, self.dbengine_listener = create_engines(dsn=self.dsn, echo_sql=self.echo_sql)
        self.DbSession = create_session(self.dbengine)


def add_common_args(p: argparse.ArgumentParser):
    p.add_argument(
        '--dsn',
        default='postgresql://algernon:algernonpwd@localhost/algernondb',
        help='DSN to connect to database, e.g. postgresql://someuser:somepwd@somehost/somedb'
    )
    p.add_argument(
        '--login',
        default='algernon',
        help='Login'
    )
    p.add_argument(
        '--login-pwd',
        default='algernonpwd',
        help='Login password'
    )
    p.add_argument(
        '--echo-sql',
        action='store_true',
        help='Sent SQL is echoed to stdout'
    )
