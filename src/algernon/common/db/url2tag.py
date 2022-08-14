import sqlalchemy as sa

from algernon.common.db import OrmBase
from algernon.common.db.ormbase import BaseMixin


class Url2Tag(OrmBase, BaseMixin):
    __table_args__ = (
        sa.ForeignKeyConstraint(('url_id',), ['public.url.id']),
        sa.ForeignKeyConstraint(('tag_id',), ['public.tag.id']),
        sa.UniqueConstraint('url_id', 'tag_id'),
    )

    url_id = sa.Column(sa.Integer, nullable=False)
    tag_id = sa.Column(sa.Integer, nullable=False)
