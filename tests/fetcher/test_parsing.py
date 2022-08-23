import json

import pytest

import sqlalchemy as sa

from algernon.common.db.fetched import Fetched
from algernon.parser.simple import ParserSimple


@pytest.mark.asyncio
async def test_parser_simple(DbSession, url_id):
    with DbSession.begin() as dbsess:
        fetched = dbsess.execute(sa.select(Fetched).filter_by(url_id=url_id)).scalar_one()
        mime_type = fetched.mime_type
        encoding = fetched.encoding
        content = fetched.content
    p = ParserSimple()
    p.parse(content, mime_type, encoding)
    print(p.lang)
    print(p.title)
    print(p.description)
    print(json.dumps(p.meta, indent=4))
    # assert p.title is not None
    # assert p.description is not None
    # assert p.tags is not None
