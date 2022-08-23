import argparse
from typing import Any

from backinajiffy.mama.rc import Rc

from algernon.cli.utils import AlgnBaseCmd
from algernon.api import url as api_url
from algernon.common.exc import RecordExistsError

CMD = __name__.split('.')[-1].replace('_', '-')


def add_subcommand(sps: argparse._SubParsersAction):
    p = sps.add_parser(CMD, help='Fetch given URL from internet')
    p.add_argument(
        'url_id',
        help='ID of the record that contains the URL'
    )
    p.set_defaults(cmd=UrlFetchCmd)


class UrlFetchCmd(AlgnBaseCmd):

    async def get_result(self) -> Any:
        rc = Rc.get_instance()
        url_id = rc.g('url_id')

        sess = self.DbSessionMaker()
        sess.begin()
        try:
            fetched = await api_url.fetch(sess, url_id)
            sess.commit()
        except Exception:
            sess.rollback()
            raise
        self.lgg.info('Fetched URL', extra=dict(data=dict(id=fetched.url_id,
                                                          http_status=fetched.http_status,
                                                          mime_type=fetched.mime_type)))
