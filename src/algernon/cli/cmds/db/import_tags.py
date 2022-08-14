import argparse
import json
from typing import Any

from backinajiffy.mama.rc import Rc

from algernon.cli.utils import AlgnBaseCmd
from algernon.api import tag as api_tag

CMD = __name__.split('.')[-1].replace('_', '-')


def add_subcommand(sps: argparse._SubParsersAction):
    p = sps.add_parser(CMD, help='Import tags from a JSON list')
    p.add_argument(
        'fn',
        help='JSON file'
    )
    p.set_defaults(cmd=DbImportTagsCmd)


class DbImportTagsCmd(AlgnBaseCmd):

    async def get_result(self) -> Any:
        rc = Rc.get_instance()
        fn = rc.g('fn')

        with open(fn, 'rt', encoding='utf-8') as fp:
            tags = set(json.load(fp))
        with self.DbSession.begin() as sess:
            n = await api_tag.add_bulk(sess=sess, tags=tags, owner=self.login)
        return n
