import argparse
from typing import Any

from backinajiffy.mama.rc import Rc

from algernon.cli.utils import AlgnBaseCmd
from algernon.api import url as api_url
from algernon.common.exc import RecordExistsError

CMD = __name__.split('.')[-1].replace('_', '-')


def add_subcommand(sps: argparse._SubParsersAction):
    p = sps.add_parser(CMD, help='Adds given URL to the database')
    p.add_argument(
        'url',
        help='The URL'
    )
    p.set_defaults(cmd=UrlAddCmd)


class UrlAddCmd(AlgnBaseCmd):

    async def get_result(self) -> Any:
        rc = Rc.get_instance()
        url = rc.g('url')

        id_ = None
        sess = self.DbSessionMaker()
        sess.begin()
        try:
            id_ = await api_url.add(sess=sess, url=url, owner=self.login)
            sess.commit()
        except RecordExistsError as e:
            self.lgg.error(e)
        except Exception as e:
            sess.rollback()
            raise
        return id_
