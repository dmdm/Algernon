from typing import Optional

import aiohttp

from algernon.common.utils import multidict_to_dict


class TikaSrv:

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.timeout = aiohttp.ClientTimeout(total=60)
        self.user_agent = 'Chrome'
        self.headers = {
            'User-Agent': self.user_agent,
            'Accept': 'application/json'
        }
        self.sess = aiohttp.ClientSession(
            base_url=self.base_url,
            timeout=self.timeout,
            headers=self.headers,
            raise_for_status=True
        )

    async def destroy(self):
        await self.sess.close()

    async def meta(self, data, content_type: Optional[str] = None) -> dict:
        url = '/meta'
        return await self._put(url, data, content_type=content_type)

    async def analyse(self, data, content_type: Optional[str] = None) -> dict:
        url = '/tika/text'
        return await self._put(url, data, content_type=content_type)

    async def _put(self, url, data, content_type: Optional[str] = None) -> dict:
        headers = {}
        if content_type:
            headers['Content-Type'] = content_type
        async with self.sess.put(url, data=data, headers=headers) as resp:
            print(multidict_to_dict(resp.request_info.headers))
            print(multidict_to_dict(resp.headers))
            return await resp.json()
