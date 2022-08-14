import argparse
import asyncio
from typing import Any

from backinajiffy.mama.cli import default_main, make_default_arg_parser
from backinajiffy.mama import cli
from backinajiffy.mama.rc import Rc

from algernon.common.const import PROJECT_NAME, PROJECT_LOGGER_NAME
from algernon.common.db.utils import DbListener, create_engines
from algernon.common.models import DbNotificationChannel
from algernon.cli.utils import add_common_args
from algernon.fetcher.worker import FetcherWorker


class StartCmd(cli.BaseCmd):

    async def get_result(self) -> Any:
        rc = Rc.get_instance()
        dsn = rc.g('dsn')
        echo_sql = rc.g('echo_sql')

        await self.start(dsn, echo_sql)
        return True

    async def start(self, dsn, echo_sql):
        eng, eng_listener = create_engines(dsn, echo_sql)
        queue = asyncio.Queue()
        listener = DbListener(channels=[DbNotificationChannel.job], queue=queue, timeout=5)
        fetcher = FetcherWorker(queue=queue, engine=eng)
        with eng_listener.connect() as conn_listener:
            listener.set_connection(conn_listener)
            await asyncio.gather(fetcher.start(), listener.start())


async def init(args: argparse.Namespace):
    args.cmd = StartCmd


async def amain(argv=None):

    arg_parser = make_default_arg_parser(project_name=PROJECT_NAME,
                                         cmd_module=None
                                         )
    add_common_args(arg_parser)

    await default_main(
        project_name=PROJECT_NAME,
        project_logger_name=PROJECT_LOGGER_NAME,
        argparser=arg_parser,
        argv=argv,
        debug_args=True,
        log_libs=[],
        init_func=init
    )


def main():
    asyncio.run(amain())


if __name__ == '__main__':
    main()
