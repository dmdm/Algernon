# FIXME THIS IS A STUB!!Replace with proper implementation!


def hash_pwd(pwd: str) -> bytes:
    hash = pwd.encode('utf-8')
    return hash


def verify_pwd(pwd: str, hash: bytes) -> bool:
    this_hash = hash_pwd(pwd)
    return this_hash == hash
