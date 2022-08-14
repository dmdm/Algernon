from sqlalchemy import orm

from algernon.common.db.url import Url
from algernon.common.db.utils import dbnotify
from algernon.common.models import DbNotificationChannel, NewUrlPayload


async def add(sess: orm.Session, url: str, owner: str):
    u = Url.create(url=url, owner=owner)
    sess.add(u)
    sess.flush()
    n = NewUrlPayload(url_id=u.id)
    await dbnotify(sess=sess, channel=DbNotificationChannel.job, payload=n)
    return u.id
