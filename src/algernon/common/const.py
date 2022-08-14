from pathlib import Path

import toml


def read_toml():
    fn = Path(__file__).parent.parent.parent.parent / 'pyproject.toml'
    with open(fn, 'rt', encoding='utf-8') as fp:
        return toml.load(fp)


t = read_toml()

PROJECT_NAME = t['tool']['poetry']['name'].lower()
PROJECT_VERSION = t['tool']['poetry']['version']
PROJECT_DESCRIPTION = t['tool']['poetry']['description']
PROJECT_LOGGER_NAME = PROJECT_NAME
