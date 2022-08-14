import argparse
import json
from typing import Any
from urllib.parse import urlsplit

import sqlalchemy as sa

from backinajiffy.mama.rc import Rc

from algernon.cli.utils import AlgnBaseCmd
from algernon.api import tag as api_tag
from algernon.common.db.cstm import Cstm
from algernon.common.db.tag import Tag
from algernon.common.db.url import Url
from algernon.common.db.url2tag import Url2Tag

CMD = __name__.split('.')[-1].replace('_', '-')


def add_subcommand(sps: argparse._SubParsersAction):
    p = sps.add_parser(CMD, help='Import bookmarks from a JSON list')
    p.add_argument(
        'fn',
        help='JSON file'
    )
    p.set_defaults(cmd=DbImportBookmarksCmd)


class DbImportBookmarksCmd(AlgnBaseCmd):

    async def get_result(self) -> Any:
        rc = Rc.get_instance()
        fn = rc.g('fn')

        with open(fn, 'rt', encoding='utf-8') as fp:
            bmm = json.load(fp)
        tags = {}
        seen = {}
        with self.DbSession.begin() as sess:
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
                u = Url.create(url=bm['href'], owner=self.login)
                sess.add(u)
                sess.flush()
                for t in bm['tags']:
                    sess.add(Url2Tag(url_id=u.id, tag_id=tags[t], owner=self.login))
                sess.add(Cstm(url_id=u.id, title=bm['title'], owner=self.login))
        for k, v in seen.items():
            if v > 1:
                print(k, v)
        return len(bmm)
