import argparse
from typing import Any

from backinajiffy.mama.rc import Rc

from algernon.cli.utils import AlgnBaseCmd
from algernon.api import tag as api_tag

CMD = __name__.split('.')[-1].replace('_', '-')


def add_subcommand(sps: argparse._SubParsersAction):
    p = sps.add_parser(CMD, help='Renames tag')
    p.add_argument(
        'old-tag',
        help='The old tag'
    )
    p.add_argument(
        'new-tag',
        help='The new tag'
    )
    p.set_defaults(cmd=TagRenameCmd)


class TagRenameCmd(AlgnBaseCmd):

    async def get_result(self) -> Any:
        rc = Rc.get_instance()
        old_tag = rc.g('old-tag')
        new_tag = rc.g('new-tag')

        with self.DbSession.begin() as sess:
            id_ = await api_tag.rename(sess=sess, old_tag=old_tag, new_tag=new_tag)
        return id_
