import asyncio
import enum
import logging
import multiprocessing
from typing import Union

import aiohttp
import sqlalchemy as sa
from sqlalchemy import orm
from yarl import URL

from algernon.common.const import PROJECT_LOGGER_NAME
from algernon.common.db.url import Url
from algernon.common.db.utils import create_engines
from algernon.common.utils import EndlessTask, json_serializer, multidict_to_dict




# class FetcherWorker(EndlessTask):
#
#     def __init__(self, queue: Union[asyncio.Queue, multiprocessing.Queue], engine: sa.engine.Engine):
#         super().__init__(queue)
#         self.lgg = logging.getLogger(PROJECT_LOGGER_NAME + '.' + self.__class__.__name__)
#         self.engine = engine
#         self.DbSession = orm.sessionmaker(engine)
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
#                           'Chrome/104.0.0.0 Safari/537.36'
#         }
#         self.http_session = aiohttp.ClientSession(
#             headers=headers,
#             json_serialize=json_serializer(),
#             timeout=aiohttp.ClientTimeout(total=300),
#         )
#
#
#     async def _run(self):
#         await asyncio.sleep(2)
#         await self.process_new_url(22)
#         # while True:
#         #     noti: DbNotification = await self.q.get()
#         #     if noti == 'STOP':
#         #         break
#         #     if noti.channel == DbNotificationChannel.job and isinstance(noti.payload, NewUrlPayload):
#         #         print('HEY!', noti)
#         #         await self.process_new_url(noti.payload.url_id)
#         #     else:
#         #         pass  # silently ignore notifications that are not about new URLs
#         #     await asyncio.sleep(0)
#
#     async def process_new_url(self, url_id: int):
#         with self.DbSession.begin() as dbsess:
#             u = dbsess.query(Url).filter_by(id=url_id).one()
#             url = URL(u.url, encoded=True)
#             owner = u.owner
#         print('##################', url)
#         async with self.http_session.get(url) as resp:
#             hh_req = multidict_to_dict(resp.request_info.headers)
#             hh_resp = multidict_to_dict(resp.headers)
#             content = await resp.read()
#             self.lgg.debug('!!!!!!!!!!!!!!status: {}'.format(resp.status))
#             self.lgg.debug('!!!!!!!!!!!!!!req headers: {}'.format(hh_req))
#             self.lgg.debug('!!!!!!!!!!!!!!resp headers: {}'.format(hh_resp))
#             self.lgg.debug('!!!!!!!!!!!!!!content: {}'.format(content))
#         await self.http_session.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)


    async def run():
        q = asyncio.Queue()
        engine, _ = create_engines('postgresql://algernon:algernonpwd@localhost/algernondb', True)
        f = FetcherWorker(queue=q, engine=engine)
        await f.process_new_url(22)


    asyncio.run(run())
