import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg

from algernon.common.db import OrmBase
from algernon.common.db.ormbase import BaseMixin


class Parsed(OrmBase, BaseMixin):
    """
    Parsed resources.

    The parser stores its result here.
    """
    __table_args__ = (
        sa.ForeignKeyConstraint(('url_id',), ['public.url.id']),
        sa.UniqueConstraint('url_id'),
    )

    url_id = sa.Column(sa.Integer, nullable=False)
    parsed = sa.Column(sa.DateTime(timezone=True), nullable=False)
    reparse = sa.Column(sa.DateTime(timezone=True))
    error = sa.Column(pg.JSONB)
    title = sa.Column(sa.String(255))
    description = sa.Column(sa.String)
    meta = sa.Column(pg.JSONB)
