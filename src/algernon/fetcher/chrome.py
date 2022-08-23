from algernon.fetcher.abc import FetcherABC


class FetcherChrome(FetcherABC):

    def __int__(self, headers=None, timeout=300):
        super().__init__(headers=headers, timeout=timeout)
        raise NotImplementedError('TODO')

    async def fetch(self, url: str):
        raise NotImplementedError('TODO')
