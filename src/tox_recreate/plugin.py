from functools import lru_cache
from hashlib import sha512
from pathlib import Path

import pluggy

hookimpl = pluggy.HookimplMarker("tox")


@lru_cache(maxsize=None)
def cached_hash_path(envconfig):
    """Return the path to envconfig's cached hash file."""
    return Path(envconfig.envdir) / "tox_recreate.hash"


@lru_cache(maxsize=None)
def cached_hash(envconfig):
    """Return envconfig's cached hash."""
    try:
        return cached_hash_path(envconfig).read_text()
    except FileNotFoundError:
        return None


def get_setup_cfg_path():  # pragma: no cover
    """Return the path to the project's setup.cfg file."""
    return Path("setup.cfg")


@lru_cache(maxsize=None)
def current_hash():
    """Return the current hash of the setup.cfg file."""
    hashobj = sha512()
    hashobj.update(get_setup_cfg_path().read_bytes())
    return hashobj.hexdigest()


@hookimpl
def tox_configure(config):
    """Trigger recreation of the venvs if setup.cfg has changed."""
    for envconfig in config.envconfigs.values():
        if envconfig.envname not in config.envlist:
            continue

        if cached_hash(envconfig) != current_hash():
            envconfig.recreate = True

    return config


@hookimpl
def tox_runtest_pre(venv):
    """Cache setup.cfg's hash in the venv for next time."""
    if not venv.envconfig.recreate:
        return

    cached_hash_path(venv.envconfig).write_text(current_hash())
