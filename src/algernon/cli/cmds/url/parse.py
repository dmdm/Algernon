import argparse
import os
from typing import Any

from backinajiffy.mama.rc import Rc

from algernon.cli.utils import AlgnBaseCmd
from algernon.api import url as api_url
from algernon.common.exc import RecordExistsError
from algernon.parser.tikasrv import TikaSrv

CMD = __name__.split('.')[-1].replace('_', '-')


def add_subcommand(sps: argparse._SubParsersAction):
    p = sps.add_parser(CMD, help='Fetch given URL from internet')
    p.add_argument(
        '--use-tika',
        action='store_true',
        help='If set, we will use Tika for parsing'
    )
    p.add_argument(
        'url_id',
        help='ID of the record that contains the URL'
    )
    p.set_defaults(cmd=UrlParseCmd)


class UrlParseCmd(AlgnBaseCmd):

    async def get_result(self) -> Any:
        rc = Rc.get_instance()
        url_id = rc.g('url_id')
        use_tika = rc.g('use_tika')

        tikasrv = TikaSrv(self.tika_url)
        sess = self.DbSessionMaker()
        sess.begin()
        try:
            parsed = await api_url.parse(sess, url_id, tikasrv=tikasrv if use_tika else None)
            sess.commit()
        except Exception:
            sess.rollback()
            raise
        finally:
            await tikasrv.destroy()
        self.lgg.info('Parsed URL', extra=dict(data=dict(id=parsed.url_id,
                                                         title=parsed.title)))
