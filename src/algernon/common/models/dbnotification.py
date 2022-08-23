from dataclasses import dataclass
from datetime import datetime
from enum import Enum, unique
from typing import Dict

from ..dataclassutils import dataclass_deserialize_enums


@dataclass
class DbNotificationPayload:
    pass


@dataclass
class FetchUrlPayload(DbNotificationPayload):
    url_id: int

    @classmethod
    def from_dict(cls, d: Dict) -> 'FetchUrlPayload':
        dataclass_deserialize_enums(cls, d)
        return cls(**d)


@unique
class DbNotificationChannel(Enum):
    job = 'job'
    test = 'test'


@dataclass
class DbNotification:
    """
    Encapsulates all properties of a Postgres notification.
    """
    rcv_time: datetime
    """Time when this notification was received"""
    pid: int
    """PID of the Postgres daemon"""
    channel: DbNotificationChannel
    """Name of the channel on which the notification came in"""
    payload: DbNotificationPayload
    """Yes"""
