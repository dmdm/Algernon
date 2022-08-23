import os
from typing import Tuple

import pytest
from pytest_httpserver import HTTPServer
import sqlalchemy as sa

from algernon.common.db.utils import create_engines, create_session_maker


@pytest.fixture(scope='session')
def httpsrv(httpserver: HTTPServer):
    httpserver.expect_request("/foobar").respond_with_json({"foo": "bar"})
    return httpserver


@pytest.fixture(scope='session')
def dsn():
    # FIXME Create fixture DB from algernon.pgdump before running the tests
    return os.environ.get('ALGERNON_DSN', 'postgresql://algernon:algernonpwd@localhost/algernondb')


@pytest.fixture(scope='session')
def dbengines(dsn) -> Tuple[sa.engine.Engine, sa.engine.Engine]:
    return create_engines(dsn=dsn, echo_sql=False)


@pytest.fixture(scope='session')
def DbSessionMaker(dbengines):
    return create_session_maker(dbengines[0])


@pytest.fixture(scope='session')
def url_id():
    return 468
