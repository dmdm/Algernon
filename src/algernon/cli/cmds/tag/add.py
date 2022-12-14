import argparse
from typing import Any

from backinajiffy.mama.rc import Rc

from algernon.cli.utils import AlgnBaseCmd
from algernon.api import tag as api_tag

CMD = __name__.split('.')[-1].replace('_', '-')


def add_subcommand(sps: argparse._SubParsersAction):
    p = sps.add_parser(CMD, help='Adds tag')
    p.add_argument(
        'tag',
        help='The tag'
    )
    p.set_defaults(cmd=TagAddCmd)


class TagAddCmd(AlgnBaseCmd):

    async def get_result(self) -> Any:
        rc = Rc.get_instance()
        tag = rc.g('tag')

        with self.DbSessionMaker.begin() as sess:
            id_ = await api_tag.add(sess=sess, tag=tag, owner=self.login)
        return id_
