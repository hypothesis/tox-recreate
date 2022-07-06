import json
from functools import lru_cache
from hashlib import sha512
from pathlib import Path

import pluggy

hookimpl = pluggy.HookimplMarker("tox")


@lru_cache
def cached_hashes_path(envconfig):
    """Return the path to envconfig's cached hashes file."""
    return Path(envconfig.envdir) / "tox_recreate.json"


@lru_cache
def cached_hashes(envconfig):
    """Return envconfig's cached hashes dict."""
    try:
        with open(
            cached_hashes_path(envconfig), "r", encoding="utf8"
        ) as cached_hashes_file:
            return json.load(cached_hashes_file)
    except FileNotFoundError:
        return {}


@lru_cache
def cached_hash(envconfig, path):
    """Return envconfig's cached hash for `path` or None."""
    return cached_hashes(envconfig).get(path)


@lru_cache
def current_hash(path):
    """Return the current hash of the file at `path`."""
    hashobj = sha512()

    with open(path, "rb") as file:
        hashobj.update(file.read())

    return hashobj.hexdigest()


@hookimpl
def tox_configure(config):
    """Trigger recreation of the venvs if setup.cfg has changed."""
    for envconfig in config.envconfigs.values():
        if envconfig.envname not in config.envlist:
            continue

        if cached_hash(envconfig, "setup.cfg") != current_hash("setup.cfg"):
            envconfig.recreate = True

    return config


@hookimpl
def tox_runtest_pre(venv):
    """Cache setup.cfg's hash in the venv for next time."""
    envconfig = venv.envconfig

    if not envconfig.recreate:
        return

    if cached_hash(envconfig, "setup.cfg") != current_hash("setup.cfg"):
        cached_hashes_ = cached_hashes(envconfig)
        cached_hashes_["setup.cfg"] = current_hash("setup.cfg")
        with open(cached_hashes_path(envconfig), "w", encoding="utf8") as file:
            json.dump(cached_hashes_, file)
