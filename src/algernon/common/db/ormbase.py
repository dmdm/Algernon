import sqlalchemy as sa
from sqlalchemy import orm

mapper_registry = orm.registry()
OrmBase = mapper_registry.generate_base(name='OrmBase')

convention = {
    "pk": "pk_%(table_name)s",
    "ix": 'ix_%(table_name)s_%(column_0_N_name)s',
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "fk": "fk_%(table_name)s_%(column_0_N_name)s_%(referred_table_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
}
OrmBase.metadata.naming_convention = convention
OrmBase.metadata.schema = 'public'


@orm.declarative_mixin
class BaseMixin:
    @orm.declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = sa.Column(sa.Integer, sa.Identity(start=1, cycle=True), primary_key=True, nullable=False)
    ctime = sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=sa.sql.func.now())

    @orm.declared_attr
    def owner(cls):
        return sa.Column(sa.String(32), sa.ForeignKey('public.algnuser.login'), nullable=False)

    mtime = sa.Column(sa.DateTime(timezone=True), nullable=True)

    @orm.declared_attr
    def editor(cls):
        return sa.Column(sa.String(32), sa.ForeignKey('public.algnuser.login'))
