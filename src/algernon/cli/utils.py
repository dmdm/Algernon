import argparse
import json
import logging
import os
from pathlib import Path
from typing import Optional, Tuple
from urllib.parse import urlsplit


import sqlalchemy as sa
from sqlalchemy import orm

from backinajiffy.mama import cli
from backinajiffy.mama.exc import MamaError
from backinajiffy.mama.rc import Rc

from algernon.common.db.utils import create_engines, create_session_maker
from algernon.api import tag as api_tag
from algernon.common.db.cstm import Cstm
from algernon.common.db.tag import Tag
from algernon.common.db.url import Url
from algernon.common.db.url2tag import Url2Tag


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
        self.tika_url = rc.g('tika_url')
        self.dbengine, self.dbengine_listener = create_engines(dsn=self.dsn, echo_sql=self.echo_sql)
        self.DbSessionMaker = create_session_maker(self.dbengine)


def add_common_args(p: argparse.ArgumentParser):
    p.add_argument(
        '--dsn',
        default=os.environ.get('ALGERNON_DSN', 'postgresql://algernon:algernonpwd@localhost/algernondb'),
        help='DSN to connect to database, e.g. postgresql://someuser:somepwd@somehost/somedb'
    )
    p.add_argument(
        '--tika-url',
        default=os.environ.get('ALGERNON_TIKA', 'http://localhost:9998/'),
        help='Base URL to connect Tika server'
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


async def import_tags(fn: Path, DbSessionMaker: orm.Session, owner: str) -> int:
    with open(fn, 'rt', encoding='utf-8') as fp:
        tags = set(json.load(fp))
    with DbSessionMaker.begin() as sess:
        n = await api_tag.add_bulk(sess=sess, tags=tags, owner=owner)
    return n


async def import_bookmarks(fn: Path, DbSessionMaker: orm.Session, owner: str) -> int:
    with open(fn, 'rt', encoding='utf-8') as fp:
        bmm = json.load(fp)
    tags = {}
    seen = {}
    with DbSessionMaker.begin() as sess:
        for t in sess.execute(sa.select(Tag)).scalars().all():
            tags[t.tag] = t.id
        for bm in bmm:
            if '://' not in bm['href']:
                continue
            u = urlsplit(bm['href'])
            uk = (u.scheme, u.netloc, u.path, u.query, u.fragment)
            if uk in seen:
                seen[uk] += 1
                continue
            else:
                seen[uk] = 1
            u = Url.create(url=bm['href'], owner=owner)
            sess.add(u)
            sess.flush()
            for t in bm['tags']:
                sess.add(Url2Tag(url_id=u.id, tag_id=tags[t], owner=owner))
            sess.add(Cstm(url_id=u.id, title=bm['title'], owner=owner))
    for k, v in seen.items():
        if v > 1:
            print(k, v)
    return len(bmm)
