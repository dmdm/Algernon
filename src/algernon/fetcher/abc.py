import abc
import logging

from algernon.common.const import PROJECT_LOGGER_NAME


class FetcherABC(abc.ABC):

    def __init__(self, headers=None, timeout=300):
        self.lgg = logging.getLogger(PROJECT_LOGGER_NAME + '.' + self.__class__.__name__)
        if headers is None:
            headers = {}
        self.headers = headers
        self.timeout = timeout
        self.req_headers = None
        self.resp_headers = None
        self.content = None
        self.http_status = None
        self.content_type = None
        self.mime_type = None
        self.encoding = None
        self.content_length = None

    @abc.abstractmethod
    async def fetch(self, url: str):
        pass
