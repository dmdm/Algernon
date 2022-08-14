import asyncio

from backinajiffy.mama.cli import default_main, make_default_arg_parser

from algernon.cli.utils import add_common_args
from algernon.common.const import PROJECT_NAME, PROJECT_LOGGER_NAME


async def amain(argv=None):
    from algernon.cli import cmds
    p = make_default_arg_parser(project_name=PROJECT_NAME,
                                cmd_module=cmds
                                )
    add_common_args(p)
    await default_main(
        project_name=PROJECT_NAME,
        project_logger_name=PROJECT_LOGGER_NAME,
        argparser=p,
        argv=argv,
        debug_args=True,
        log_libs=[]
    )


def main():
    asyncio.run(amain())


if __name__ == '__main__':
    main()
