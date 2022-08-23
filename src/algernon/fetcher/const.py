import enum


@enum.unique
class UserAgent(enum.Enum):
    chrome = 0
    firefox = 1
    safari = 2


USER_AGENTS = {
    UserAgent.chrome: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/104.0.0.0 Safari/537.36'
}
