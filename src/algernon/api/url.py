from typing import Optional

import psycopg2.errors as dbapiexc
import sqlalchemy as sa
from sqlalchemy import orm
import sqlalchemy.exc as saexc

from algernon.api.notify import notify_fetch_url
from algernon.common.db.fetched import Fetched
from algernon.common.db.parsed import Parsed
from algernon.common.db.url import Url
from algernon.common.exc import RecordExistsError
from algernon.fetcher.persisting import PersistingFetcher
from algernon.fetcher.simple import FetcherSimple
from algernon.parser.persisting import PersistingParser
from algernon.parser.simple import ParserSimple
from algernon.parser.tika import ParserTika
from algernon.parser.tikasrv import TikaSrv


async def add(sess: orm.Session, url: str, owner: str) -> int:
    """
    Adds new URL to database and notifies fetcher.

    N.B. Caller cannot use context manager for session, because we here handle Unique Key violations and start a new
    transaction.

    :param sess: A database session
    :param url: The URL to add
    :param owner: User that owns this record
    :return: ID of inserted record
    :raise RecordExistsError: if record exists.
    """
    u = Url.create(url=url, owner=owner)
    sess.add(u)
    try:
        sess.flush()
    except saexc.IntegrityError as e:
        if isinstance(e.orig, dbapiexc.UniqueViolation):
            sess.rollback()
            sess.begin()
            u = sess.execute(sa.select(Url).filter_by(url=url)).scalar_one()
            raise RecordExistsError(u.id, f'URL exists: "{url}"') from e
        else:
            raise
    await notify_fetch_url(sess=sess, url_id=u.id)
    return u.id


async def fetch(sess: orm.Session, url_id: int) -> Fetched:
    fetcher = FetcherSimple()
    pf = PersistingFetcher(fetcher)
    await pf.fetch(sess=sess, url_id=url_id)
    fetched = sess.execute(sa.select(Fetched).filter_by(url_id=url_id)).scalar_one()
    return fetched


async def parse(sess: orm.Session, url_id: int, tikasrv: Optional[TikaSrv] = None) -> Parsed:
    if tikasrv:
        p = ParserTika(tikasrv)
    else:
        p = ParserSimple()
    pp = PersistingParser(parser=p)
    parsed = await pp.parse(sess=sess, url_id=url_id)
    return parsed
