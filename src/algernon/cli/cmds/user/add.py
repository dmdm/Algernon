import argparse
from typing import Any

from backinajiffy.mama.rc import Rc

from algernon.cli.utils import AlgnBaseCmd
from algernon.api import url as api_url, user as api_user

CMD = __name__.split('.')[-1].replace('_', '-')


def add_subcommand(sps: argparse._SubParsersAction):
    p = sps.add_parser(CMD, help='Adds user account')
    p.add_argument(
        '--pwd',
        required=True,
        help='Password'
    )
    p.add_argument(
        '--email',
        required=True,
        help='Email address'
    )
    p.add_argument(
        'user-login',
        help='Login name'
    )
    p.set_defaults(cmd=UserAddCmd)


class UserAddCmd(AlgnBaseCmd):

    async def get_result(self) -> Any:
        rc = Rc.get_instance()
        user = rc.g('user-login')
        pwd = rc.g('pwd')
        email = rc.g('email')

        with self.DbSessionMaker.begin() as sess:
            id_ = await api_user.add(sess=sess, login=user, pwd=pwd, email=email, owner=self.login)
        return id_
