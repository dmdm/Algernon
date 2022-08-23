import pytest

import sqlalchemy as sa

from algernon.common.db.fetched import Fetched
from algernon.fetcher.persisting import PersistingFetcher
from algernon.fetcher.simple import FetcherSimple


@pytest.mark.asyncio
async def test_fetcher_persisting_1(DbSession, url_id):
    fetcher = FetcherSimple()
    pf = PersistingFetcher(fetcher)
    await pf.fetch(DbSession=DbSession, url_id=url_id)
    with DbSession.begin() as dbsess:
        fetched = dbsess.execute(sa.select(Fetched).filter_by(url_id=url_id)).scalar_one()
        assert fetched is not None
        assert fetched.url_id == url_id
        assert fetched.visited is not None
        assert fetched.req_headers is not None
        assert fetched.resp_headers is not None
        assert fetched.content is not None
