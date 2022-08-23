import asyncio
import logging
import multiprocessing
import select
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Union, Optional, Tuple
import json

import sqlalchemy as sa
from sqlalchemy import orm

from algernon.common.classmaps import dataclass_from_dict
from algernon.common.const import PROJECT_LOGGER_NAME
from algernon.common.dataclassutils import dataclass_to_dict
from algernon.common.db import OrmBase
from algernon.common.models import DbNotificationChannel, DbNotification, DbNotificationPayload
from algernon.common.utils import EndlessTask, json_deserializer, json_serializer
from algernon.api import user as api_user


class DbListener(EndlessTask):

    def __init__(self,
                 channels: List[DbNotificationChannel],
                 queue: Union[asyncio.Queue, multiprocessing.Queue],
                 timeout=5):
        """
        Listens for Postgres NOTIFY.

        Enqueues received notification in given queue.

        Nota bene: The listener should run on a separate connection than the notifier.

        :param conn: An open connection
        :param channels: List of channel names to listen to
        :param queue: This queue gets the payload
        :param timeout: Timeout for the socket select()
        """
        super().__init__(queue=queue)
        self.conn: Optional[sa.engine.Connection] = None
        self.channels = channels
        self.timeout = timeout
        self.lgg = logging.getLogger(PROJECT_LOGGER_NAME + '.' + self.__class__.__name__)

    def set_connection(self, conn: sa.engine.Connection):
        self.conn = conn

    async def start(self):
        self.lgg.debug('Starting')
        self._listen()
        await super().start()

    def stop(self):
        self.lgg.debug('Stopping')
        super().stop()
        self._unlisten()

    def kill(self):
        self.lgg.debug('Killing')
        super().kill()
        self._unlisten()

    def _listen(self):
        for ch in self.channels:
            self.conn.execute(sa.text(f'LISTEN {ch.value}'))

    def _unlisten(self):
        for ch in self.channels:
            self.conn.execute(sa.text(f'UNLISTEN {ch.value}'))

    async def _run(self):
        if select.select([self.conn.connection], [], [], self.timeout) == ([], [], []):
            # Shall we log these timeouts or just silently pass?
            # self.lgg.debug("Waiting for DB notification timed out")
            # print("*********************** Waiting for DB notification timed out")
            pass
        else:
            self.conn.connection.poll()
            while self.conn.connection.notifies:
                raw_n = self.conn.connection.notifies.pop()
                try:
                    n = DbNotification(
                        rcv_time=datetime.now(tz=timezone.utc),
                        pid=raw_n.pid,
                        channel=DbNotificationChannel(raw_n.channel),
                        payload=dataclass_from_dict(json_deserializer()(raw_n.payload))
                    )
                    self.lgg.debug('Received notification', extra=dict(data=dataclass_to_dict(n)))
                except (KeyError, json.decoder.JSONDecodeError, ValueError) as e:
                    self.lgg.error('Failed to process notification', extra=dict(data=dict(raw_n=str(raw_n), error=e)))
                else:
                    self.q.put_nowait(n)


async def dbnotify(sess: orm.Session, channel: DbNotificationChannel, payload: DbNotificationPayload):
    """
    Sends a Postgres notification.

    Caller is responsible to manage the transaction correctly; the notification is sent only when transaction is
    committed.

    :param sess: An SQLAlchemy session
    :param channel: Name of the channel to notify
    :param payload: A dict as payload
    """
    payload = json_serializer()(dataclass_to_dict(payload))
    sess.execute(sa.text(f"NOTIFY {channel.value}, '{payload}'"))


def create_engines(dsn: str, echo_sql=False) -> Tuple[sa.engine.Engine, sa.engine.Engine]:
    eng = sa.create_engine(dsn,
                           echo=echo_sql,
                           echo_pool=echo_sql,
                           json_serializer=json_serializer(),
                           json_deserializer=json_deserializer(),
                           future=True)
    eng_listener = eng.execution_options(isolation_level='AUTOCOMMIT')
    return eng, eng_listener


def create_session_maker(engine: sa.engine.Engine):
    return orm.sessionmaker(engine, future=True)


async def init_db(engine: sa.engine.Engine, DbSessionMaker: orm.Session, fn_alembic_ini: Path, drop=False):
    # need to import all orm models to ensure they are present in the metadata
    from algernon.common.db.algnuser import AlgnUser
    from algernon.common.db.url import Url
    from algernon.common.db.fetched import Fetched
    from algernon.common.db.parsed import Parsed
    from algernon.common.db.tag import Tag
    from algernon.common.db.url2tag import Url2Tag
    from algernon.common.db.cstm import Cstm

    if drop:
        OrmBase.metadata.drop_all(engine)

    with DbSessionMaker.begin() as sess:
        sess.execute(sa.text('''DROP COLLATION IF EXISTS "case_insensitive";
                                CREATE COLLATION "case_insensitive"''' 
                             '''(provider = icu, locale = 'und-u-ks-level2', deterministic = false)'''))

    OrmBase.metadata.create_all(engine)
    from alembic.config import Config
    from alembic import command
    alembic_cfg = Config(str(fn_alembic_ini))
    command.stamp(alembic_cfg, "head")

    with DbSessionMaker.begin() as sess:
        id_ = await api_user.add(sess=sess, login='algernon', pwd='algernonpwd', email='algernon@localhost',
                                 owner='algernon')
    return id_
