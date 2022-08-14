import argparse
from typing import Any

from backinajiffy.mama.rc import Rc

from algernon.cli.utils import AlgnBaseCmd
from algernon.api import tag as api_tag

CMD = __name__.split('.')[-1].replace('_', '-')


def add_subcommand(sps: argparse._SubParsersAction):
    p = sps.add_parser(CMD, help='Removes tag')
    p.add_argument(
        'tag',
        help='The tag'
    )
    p.set_defaults(cmd=TagRemoveCmd)


class TagRemoveCmd(AlgnBaseCmd):

    async def get_result(self) -> Any:
        rc = Rc.get_instance()
        tag = rc.g('tag')

        with self.DbSession.begin() as sess:
            id_ = await api_tag.remove(sess=sess, tag=tag)
        return id_
