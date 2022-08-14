from urllib.parse import urlsplit

import sqlalchemy as sa

from algernon.common.db import OrmBase
from algernon.common.db.ormbase import BaseMixin


class Url(OrmBase, BaseMixin):
    """
    An URL.

    To create a bookmark, user inputs an URL. We store it here, as well as its parsed constituents.
    """
    __table_args__ = (
        # Cannot simply ux(url), because we cast scheme and netloc to lower
        sa.UniqueConstraint('scheme', 'netloc', 'path', 'query', 'fragment'),
    )

    url = sa.Column(sa.String, nullable=False)
    scheme = sa.Column(sa.String(10), nullable=False)
    netloc = sa.Column(sa.String(255), nullable=False)
    path = sa.Column(sa.String, nullable=True)
    query = sa.Column(sa.String, nullable=True)
    fragment = sa.Column(sa.String, nullable=True)
    username = sa.Column(sa.String(255), nullable=True)
    password = sa.Column(sa.String(255), nullable=True)
    hostname = sa.Column(sa.String(255), nullable=True)
    port = sa.Column(sa.Integer, nullable=True)

    @classmethod
    def create(cls, url: str, owner: str) -> 'Url':
        u = urlsplit(url)
        return cls(
            url=url,
            scheme=u.scheme.lower(),
            netloc=u.netloc.lower(),
            path=u.path,
            query=u.query,
            fragment=u.fragment,
            username=u.username,
            password=u.password,
            hostname=u.hostname,
            port=u.port,
            owner=owner
        )
