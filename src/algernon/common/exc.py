from typing import Optional


class AlgernonError(Exception):
    code = 'ALGN_00000'
    pass


class AuthenticationError(AlgernonError):
    code = 'ALGN_10000'
    pass


class DbError(AlgernonError):
    code = 'ALGN_20000'
    pass


class RecordExistsError(DbError):
    code = 'ALGN_20010'

    def __init__(self, record_id: int, msg: str, *args):
        self.record_id = record_id
        super().__init__(msg, *args)

    def __str__(self):
        return f'[{self.__class__.code}] {self.__class__.__name__}: {self.args[0]}, record ID: {self.record_id}'


class FetchedNotFoundError(DbError):
    code = 'ALGN_20020'

    def __init__(self, url_id: int, msg: Optional[str] = None, *args):
        self.url_id = url_id
        if not msg:
            msg = 'Record "fetched" not found for URL'
        super().__init__(msg, *args)

    def __str__(self):
        return f'[{self.__class__.code}] {self.__class__.__name__}: {self.args[0]}, URL ID: {self.url_id}'


class FetcherError(AlgernonError):
    code = 'ALGN_30000'
    pass


class ParserError(AlgernonError):
    code = 'ALGN_40000'
    pass
