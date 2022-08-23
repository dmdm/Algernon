import abc
import logging
from typing import Optional

from algernon.common.const import PROJECT_LOGGER_NAME
from algernon.parser.exc import ParserError


class ParserABC(abc.ABC):

    def __init__(self):
        self.lgg = logging.getLogger(PROJECT_LOGGER_NAME + '.' + self.__class__.__name__)
        self.lang: Optional[str] = None
        self.title: Optional[str] = None
        self.description: Optional[str] = None
        self.tags: Optional[list] = None
        self.meta: Optional[dict] = None
        self.error: Optional[ParserError] = None

    @abc.abstractmethod
    async def parse(self, content: bytes, mime_type: str, encoding: Optional[str] = None):
        pass
