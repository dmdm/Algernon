from sqlalchemy import orm

from algernon.common.db.algnuser import AlgnUser
from algernon.common.exc import AuthenticationError
from algernon.common.security import hash_pwd


async def add(sess: orm.Session, login: str, pwd: str, email: str, owner: str) -> int:
    h = hash_pwd(pwd)
    u = AlgnUser(login=login, pwd_hash=h, email=email, owner=owner)
    sess.add(u)
    sess.flush()
    return u.id


# TODO rewrite for 2.0

# async def login(sess: orm.Session, login: str, pwd: str) -> str:
#     h = hash_pwd(pwd)
#     u = sess.query(AlgnUser).filter_by(login=login, pwd_hash=h).one()
#     if not u:
#         raise AuthenticationError()
#     return u.login
#
#
# async def change_pwd(sess: orm.Session, login: str, new_pwd: str):
#     h = hash_pwd(new_pwd)
#     u = sess.query(AlgnUser).filter_by(login=login).one()
#     u.pwd_hash = h
