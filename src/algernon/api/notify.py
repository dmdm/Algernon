from sqlalchemy import orm

from algernon.common.db.utils import dbnotify
from algernon.common.models import DbNotificationChannel, FetchUrlPayload


async def notify_fetch_url(sess: orm.Session, url_id: int):
    n = FetchUrlPayload(url_id=url_id)
    await dbnotify(sess=sess, channel=DbNotificationChannel.job, payload=n)
