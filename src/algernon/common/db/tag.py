import re

import sqlalchemy as sa

from algernon.common.db import OrmBase
from algernon.common.db.ormbase import BaseMixin


RE_WHITESPACE = re.compile(r'\s+')


class Tag(OrmBase, BaseMixin):
    __table_args__ = (
        sa.UniqueConstraint('tagci'),
    )

    tag = sa.Column(sa.String(255), nullable=False)
    tagci = sa.Column(sa.String(255, collation='case_insensitive'), nullable=False)

    @classmethod
    def create(cls, tag: str, owner: str):
        tag = RE_WHITESPACE.sub(' ', tag.strip())
        return cls(tag=tag, tagci=tag, owner=owner)
