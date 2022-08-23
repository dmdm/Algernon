import pytest

from algernon.fetcher.persisting import PersistingFetcher
from algernon.fetcher.simple import FetcherSimple


@pytest.mark.asyncio
async def test_fetcher_persisting_1(DbSessionMaker, url_id):
    fetcher = FetcherSimple()
    pf = PersistingFetcher(fetcher)
    with DbSessionMaker.begin() as sess:
        fetched = await pf.fetch(sess=sess, url_id=url_id)
        assert fetched is not None
        assert fetched.url_id == url_id
        assert fetched.visited is not None
        assert fetched.req_headers is not None
        assert fetched.resp_headers is not None
        assert fetched.content is not None
