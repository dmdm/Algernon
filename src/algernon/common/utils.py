import asyncio
import functools
import json
import logging
import multiprocessing
from typing import Any, Union, Optional, Tuple


def module_logger() -> logging.Logger:
    return logging.getLogger(__name__)


class EndlessTask:

    def __init__(self, queue: Union[asyncio.Queue, multiprocessing.Queue]):
        self.q = queue
        self._do_stop = False
        self._do_kill = False
        self.lgg = module_logger()

    async def start(self):
        self._do_stop = False
        self._do_kill = False
        while True:
            if self._do_stop and self.q.empty():
                break
            if self._do_kill:
                break
            await self._run()
            await asyncio.sleep(0)

    async def _run(self):
        pass

    def stop(self):
        self._do_stop = True

    def kill(self):
        self._do_kill = True


def json_serializer() -> Any:
    """
    Returns a function that serializes a variable to JSON.

    This serializer handles more data types that the default json.dumps as it uses Python's :func:`str` as default.
    """
    return functools.partial(json.dumps, default=str)


def json_deserializer() -> Any:
    """Returns a function that deserializes JSON."""
    return json.loads


def multidict_to_dict(md) -> dict:
    return {k: md.getall(k) for k in md.keys()}


def parse_content_type(ct: str) -> Tuple[str, Optional[str]]:
    enc = None
    mt, field = [e.strip() for e in ct.split(';')]
    if field:
        k, v = [e.strip() for e in field.split('=')]
        if k.lower() == 'charset':
            enc = v
    return mt.lower(), enc.upper()
