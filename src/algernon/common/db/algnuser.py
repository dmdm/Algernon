import sqlalchemy as sa

from algernon.common.db import OrmBase
from algernon.common.db.ormbase import BaseMixin


class AlgnUser(OrmBase, BaseMixin):
    """
    An Algernon user.
    """
    __table_args__ = (
        sa.UniqueConstraint('login'),
    )

    login = sa.Column(sa.String(32, collation='case_insensitive'), nullable=False)
    pwd_hash = sa.Column(sa.String(128), nullable=False)
    email = sa.Column(sa.String(128), nullable=False)
