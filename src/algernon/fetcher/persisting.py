from datetime import datetime, timezone
from typing import Optional

import sqlalchemy as sa
import sqlalchemy.exc
from sqlalchemy import orm

from algernon.common.db.fetched import Fetched
from algernon.common.db.url import Url
from algernon.fetcher.abc import FetcherABC


class PersistingFetcher:

    def __init__(self, fetcher: FetcherABC):
        self.fetcher = fetcher

    async def fetch(self, sess: orm.Session, url_id: int, editor: Optional[str] = None) -> Fetched:
        now = datetime.now(tz=timezone.utc)
        u = sess.get(Url, url_id)

        try:
            fetched = sess.execute(sa.select(Fetched).filter_by(url_id=url_id)).scalar_one()
            fetched.visited = now
            fetched.editor = editor if editor else u.owner
            fetched.mtime = now
        except sa.exc.NoResultFound:
            fetched = Fetched(
                url_id=url_id,
                visited=now,
                owner=u.owner
            )
            sess.add(fetched)
            sess.flush()
        url = u.url
        fetched_id = fetched.id

        await self.fetcher.fetch(url)

        fetched = sess.get(Fetched, fetched_id)
        fetched.req_headers = self.fetcher.req_headers
        fetched.resp_headers = self.fetcher.resp_headers
        fetched.http_status = self.fetcher.http_status
        fetched.mime_type = self.fetcher.mime_type
        fetched.encoding = self.fetcher.encoding
        fetched.content_length = self.fetcher.content_length
        fetched.content = self.fetcher.content
        fetched.byte_length = len(self.fetcher.content)
        fetched.last_ok_visit = now
        return fetched
