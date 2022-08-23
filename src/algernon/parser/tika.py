import json
from typing import Optional

from algernon.parser.abc import ParserABC
from algernon.parser.tikasrv import TikaSrv


class ParserTika(ParserABC):

    def __init__(self, tikasrv: TikaSrv):
        super().__init__()
        self.tikasrv = tikasrv

    async def parse(self, content: bytes, mime_type: str, encoding: Optional[str] = None) -> dict:
        # TODO Catch HTTP error communicating with Tika and put it into self.error
        resp = await self.tikasrv.analyse(content, content_type=mime_type)
        self.title = resp.get('dc:title', resp.get('og:title', resp.get('twitter:title')))
        self.description = resp.get('dc:description', resp.get('og:description', resp.get('twitter:description')))
        self.content = resp.get('X-TIKA:content')
        del resp['X-TIKA:content']
        self.meta = resp
        print(json.dumps(resp, indent=4))
        return resp
