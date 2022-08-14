import sqlalchemy as sa
from sqlalchemy import orm

from algernon.common.db.tag import Tag


async def add(sess: orm.Session, tag: str, owner: str) -> int:
    tag = Tag.create(tag=tag, owner=owner)
    sess.add(tag)
    sess.flush()
    return tag.id


async def remove(sess: orm.Session, tag: str):
    t = sess.execute(
        sa.select(Tag).filter_by(tag=tag)
    ).scalar_one()
    id_ = t.id
    sess.delete(t)
    return id_


async def rename(sess: orm.Session, old_tag: str, new_tag: str) -> int:
    t = sess.execute(
        sa.select(Tag).filter_by(tag=old_tag)
    ).scalar_one()
    t.tag = new_tag
    return t.id


async def add_bulk(sess: orm.Session, tags: set[str], owner: str) -> int:
    tt = []
    for tag in tags:
        tt.append(Tag.create(tag=tag, owner=owner))
    sess.bulk_save_objects(tt)

    return len(tt)
