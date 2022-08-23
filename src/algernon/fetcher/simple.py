import aiohttp

from algernon.common.utils import json_serializer, multidict_to_dict
from algernon.fetcher.abc import FetcherABC
from algernon.fetcher.const import UserAgent, USER_AGENTS


class FetcherSimple(FetcherABC):

    def __init__(self, headers=None, timeout=300, user_agent=UserAgent.chrome):
        super().__init__(headers=headers, timeout=timeout)
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.user_agent = user_agent

        self.headers['User-Agent'] = USER_AGENTS[self.user_agent]
        self.http_session = aiohttp.ClientSession(
            headers=self.headers,
            json_serialize=json_serializer(),
            timeout=self.timeout,
        )

    async def fetch(self, url: str):
        async with self.http_session.get(url) as resp:
            self.http_status = resp.status
            self.req_headers = multidict_to_dict(resp.request_info.headers)
            self.resp_headers = multidict_to_dict(resp.headers)
            self.content_type = resp.headers.get('content-type')
            self.mime_type = resp.content_type
            self.encoding = resp.charset
            self.content_length = resp.content_length
            self.content = await resp.read()
        await self.http_session.close()
