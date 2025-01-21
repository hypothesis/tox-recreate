from unittest.mock import MagicMock

import pytest

from tox_recreate import plugin


class TestToxConfigure:
    def test_when_theres_no_cached_hash_file(self, config):
        plugin.tox_configure(config)

        assert config.envconfigs["test"].recreate is True

    def test_when_the_hash_doesnt_match(self, config, cached_hash_path):
        cached_hash_path.write_text("wrong_hash")

        plugin.tox_configure(config)

        assert config.envconfigs["test"].recreate is True

    def test_when_the_hash_matches(self, config, cached_hash_path, expected_hash):
        cached_hash_path.write_text(expected_hash)

        plugin.tox_configure(config)

        assert not config.envconfigs["test"].recreate

    @pytest.fixture
    def config(self, make_envconfig):
        """Return a mock tox Config object."""
        return MagicMock(
            spec_set=["envconfigs", "envlist"],
            envconfigs={
                "format": make_envconfig("format"),
                "test": make_envconfig("test"),
            },
            envlist=["test"],
        )

    @pytest.fixture
    def cached_hash_path(self, config):
        """Return the path to the cached hash file."""
        return get_cached_hash_path(config.envconfigs["test"])


class TestToxRuntestPre:
    def test_it_caches_the_hash(self, expected_hash, venv):
        venv.envconfig.recreate = True

        plugin.tox_runtest_pre(venv)

        assert get_cached_hash_path(venv.envconfig).read_text() == expected_hash

    def test_it_doesnt_cache_the_hash_if_the_venv_wasnt_updated(self, venv):
        plugin.tox_runtest_pre(venv)

        assert not get_cached_hash_path(venv.envconfig).exists()

    @pytest.fixture
    def venv(self, make_envconfig):
        return MagicMock(spec_set=["envconfig"], envconfig=make_envconfig("lint"))


def get_cached_hash_path(envconfig):
    """Return the patch to envconfig's cached hash file."""
    return envconfig.envdir / "tox_recreate.hash"


@pytest.fixture
def make_envconfig(tmp_path):
    def make_envconfig(envname):
        """Return a mock tox TestenvConfig object."""
        envconfig = MagicMock(
            spec_set=["envname", "envdir", "recreate"],
            envname=envname,
            envdir=tmp_path / envname,
            recreate=False,
        )
        envconfig.envdir.mkdir(parents=True, exist_ok=True)
        return envconfig

    return make_envconfig


@pytest.fixture(autouse=True)
def get_setup_cfg_path(mocker, tmp_path):
    """Patch plugin.py so that it reads the test setup.cfg file."""
    return mocker.patch(
        "tox_recreate.plugin.get_setup_cfg_path",
        return_value=tmp_path / "setup.cfg",
    )


@pytest.fixture(autouse=True)
def get_pyrpoject_toml_path(mocker, tmp_path):
    """Patch plugin.py so that it reads the test pyproject.toml file."""
    return mocker.patch(
        "tox_recreate.plugin.get_pyproject_toml_path",
        return_value=tmp_path / "pyproject.toml",
    )


@pytest.fixture(autouse=True)
def setup_cfg(get_setup_cfg_path):
    """Create the test setup.cfg file."""
    get_setup_cfg_path.return_value.write_text("test setup.cfg file contents")


@pytest.fixture(autouse=True)
def pyproject_toml(get_pyrpoject_toml_path):
    """Create the test pyproject.toml file."""
    get_pyrpoject_toml_path.return_value.write_text("test pyproject.toml file contents")


@pytest.fixture
def expected_hash():
    """Return the correct hash of the test setup.cfg and pyproject.toml files."""
    return "5373103a9c1d50997e43b9f007a1448f22c12d5e55314a85cf9674496b84e1eb68ae1bd24a776a862765f51824afe4219e7b91a50335bde900d3d4b04f194144"
