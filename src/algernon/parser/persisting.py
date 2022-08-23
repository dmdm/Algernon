from datetime import datetime, timezone
from typing import Optional

from algernon.common.db.fetched import Fetched
from algernon.common.db.parsed import Parsed
from algernon.common.exc import FetchedNotFoundError
from algernon.parser.abc import ParserABC


import sqlalchemy as sa
import sqlalchemy.exc
from sqlalchemy import orm


class PersistingParser:

    def __init__(self, parser: ParserABC):
        self.parser = parser

    async def parse(self, sess: orm.Session, url_id: int, editor: Optional[str] = None) -> Parsed:
        try:
            fetched = sess.execute(sa.select(Fetched).filter_by(url_id=url_id)).scalar_one()
        except sa.exc.NoResultFound as e:
            raise FetchedNotFoundError(url_id) from e
        now = datetime.now(tz=timezone.utc)

        try:
            parsed = sess.execute(sa.select(Parsed).filter_by(url_id=url_id)).scalar_one()
            parsed.parsed = now
            parsed.editor = editor if editor else fetched.owner
            parsed.mtime = now
        except sa.exc.NoResultFound:
            parsed = Parsed(
                url_id=url_id,
                parsed=now,
                owner=fetched.owner
            )
            sess.add(parsed)

        await self.parser.parse(content=fetched.content, mime_type=fetched.mime_type, encoding=fetched.encoding)

        parsed.title = self.parser.title
        parsed.description = self.parser.description
        parsed.meta = self.parser.meta
        parsed.content = self.parser.content
        parsed.error = self.parser.error  # TODO convert exception instance to JSON
        return parsed
