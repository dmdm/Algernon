from typing import Optional

from algernon.parser.abc import ParserABC


class ParserTika(ParserABC):

    def parse(self, content: bytes, mime_type: str, encoding: Optional[str] = None):
        raise NotImplementedError('TODO')
