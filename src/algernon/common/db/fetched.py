import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg

from algernon.common.db import OrmBase
from algernon.common.db.ormbase import BaseMixin


class Fetched(OrmBase, BaseMixin):
    """
    Fetched resources.

    The fetcher stores the headers of the communication, its status, and the binary body of the response here.
    Mime type and encoding are taken from the response headers.
    """
    __table_args__ = (
        sa.ForeignKeyConstraint(('url_id',), ['public.url.id'], use_alter=True),
        sa.UniqueConstraint('url_id'),
    )

    url_id = sa.Column(sa.Integer, nullable=False)
    visited = sa.Column(sa.DateTime(timezone=True), nullable=False)
    revisit = sa.Column(sa.DateTime(timezone=True))
    header_tx = sa.Column(pg.JSONB, nullable=False)
    header_rx = sa.Column(pg.JSONB)
    http_status_num = sa.Column(sa.SmallInteger)
    http_status_txt = sa.Column(sa.String)
    mime_type = sa.Column(sa.String(255))
    encoding = sa.Column(sa.String(255))
    body = sa.Column(sa.LargeBinary)
