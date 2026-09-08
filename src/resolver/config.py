import tomllib
from ipaddress import IPv4Address
from pathlib import Path
from typing import Annotated

from pydantic import Field, ValidationError

from .records import Base

# Location the .deb installs config.toml to
SYSTEM_CONFIG_PATH = Path("/var/resolver/config/config.toml")


class ConfigError(Exception):
    pass


class ResolverConfig(Base):
    dns_server: IPv4Address | None = None
    query_timeout: Annotated[float, Field(gt=0, le=30)] = 5
    retries: Annotated[int, Field(ge=0, le=10)] = 3


def load_config(cfg_path: Path | None = None) -> ResolverConfig:
    """Load config from cfg_path, else the system path, else built-in defaults."""
    path = cfg_path or SYSTEM_CONFIG_PATH

    if not path.is_file():
        if cfg_path is not None:
            raise ConfigError(f"config file not found: {path}")
        return ResolverConfig()

    try:
        with path.open("rb") as f:
            raw = tomllib.load(f)
    except (OSError, tomllib.TOMLDecodeError) as e:
        raise ConfigError(f"could not read config {path}: {e}") from e

    try:
        return ResolverConfig(**raw)
    except ValidationError as e:
        raise ConfigError(f"invalid config {path}: {e}") from e
