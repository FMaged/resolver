from ipaddress import IPv4Address

import pytest

from resolver import config as config_module
from resolver.config import ConfigError, ResolverConfig, load_config


def write_config(tmp_path, body):
    path = tmp_path / "config.toml"
    path.write_text(body)
    return path


def test_defaults_when_no_file(tmp_path, monkeypatch):
    monkeypatch.setattr(config_module, "SYSTEM_CONFIG_PATH", tmp_path / "absent.toml")
    config = load_config(None)
    assert config == ResolverConfig()
    assert config.dns_server is None
    assert config.query_timeout == 5


def test_loads_values(tmp_path):
    path = write_config(tmp_path, 'dns_server = "1.1.1.1"\nquery_timeout = 2\nretries = 0\n')
    config = load_config(path)
    assert config.dns_server == IPv4Address("1.1.1.1")
    assert config.query_timeout == 2
    assert config.retries == 0


def test_missing_explicit_file_raises(tmp_path):
    with pytest.raises(ConfigError, match="not found"):
        load_config(tmp_path / "absent.toml")


def test_unknown_key_raises(tmp_path):
    path = write_config(tmp_path, "bind_address = \"0.0.0.0\"\n")
    with pytest.raises(ConfigError, match="invalid config"):
        load_config(path)


def test_out_of_range_value_raises(tmp_path):
    path = write_config(tmp_path, "query_timeout = 99\n")
    with pytest.raises(ConfigError, match="invalid config"):
        load_config(path)


def test_malformed_toml_raises(tmp_path):
    path = write_config(tmp_path, "this is not toml\n")
    with pytest.raises(ConfigError, match="could not read"):
        load_config(path)
