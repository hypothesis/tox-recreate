from unittest.mock import MagicMock

import pytest

from tox_recreate.main import tox_configure


class TestToxConfigure:
    def test_with_no_cached_hash(self, config):
        tox_configure(config)

        assert not config.envconfigs["tests"].recreate
        assert config.envconfigs["format"].recreate

    def test_with_non_matching_cached_hash(self, config):
        pass

    def test_with_matching_cached_hash(self, config):
        envconfig = config.envconfigs["format"]
        with open(
            Path(envconfig.envdir) / "tox_recreate.json", "w", encoding="utf8"
        ) as file:
            json.dump(cached_hashes, file)

    @pytest.fixture
    def config(self, envconfig):
        return MagicMock(
            spec_set=["envconfigs", "envlist"],
            envconfigs={
                "tests": envconfig("tests"),
                "format": envconfig("format"),
            },
            envlist=["format"],
        )


@pytest.fixture
def envconfig(tmp_path):
    def envconfig(envname):
        """Return a mock tox envconfig object."""
        return MagicMock(
            spec_set=["envdir", "envname", "recreate"],
            envdir=tmp_path / envname,
            envname=envname,
            recreate=False,
        )

    return envconfig
