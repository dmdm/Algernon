import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg

from algernon.common.db import OrmBase
from algernon.common.db.ormbase import BaseMixin


class Cstm(OrmBase, BaseMixin):
    """
    Custom attributes for an URL.

    A user can override the parsed attributes, e.g. title and description.
    """
    __table_args__ = (
        sa.ForeignKeyConstraint(('url_id',), ['public.url.id']),
        sa.UniqueConstraint('url_id', 'owner'),
    )

    url_id = sa.Column(sa.Integer, nullable=False)
    title = sa.Column(sa.String(255))
    description = sa.Column(sa.String)
    meta = sa.Column(pg.JSONB)
