import aiohttp
import pytest

from algernon.fetcher.abc import FetcherABC
from algernon.fetcher.simple import FetcherSimple


def _check_fetch_result(f: FetcherABC):
    assert 200 <= f.http_status < 300
    assert f.req_headers is not None
    assert f.resp_headers is not None
    assert f.content_type is not None
    assert f.content_length > 0


@pytest.mark.asyncio
async def test_get_foobar(httpsrv):
    async with aiohttp.ClientSession() as sess:
        async with sess.get(httpsrv.url_for("/foobar")) as resp:
            assert resp.status == 200
            assert await resp.json() == {"foo": "bar"}


@pytest.mark.asyncio
async def test_fetch_examplecom():
    fetcher = FetcherSimple()
    await fetcher.fetch('http://www.example.com')
    _check_fetch_result(fetcher)


@pytest.mark.asyncio
async def test_fetch_foobar(httpsrv):
    fetcher = FetcherSimple()
    await fetcher.fetch(httpsrv.url_for("/foobar"))
    _check_fetch_result(fetcher)
