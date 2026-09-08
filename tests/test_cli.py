import pytest

from resolver.cli import build_parser


def test_defaults_to_a_record():
    args = build_parser().parse_args(["github.com"])
    assert args.name == "github.com"
    assert args.type == "A"
    assert args.config is None
    assert args.verbose is False


def test_accepts_type_and_flags():
    args = build_parser().parse_args(["github.com", "MX", "-v", "--config", "/tmp/c.toml"])
    assert args.type == "MX"
    assert args.verbose is True
    assert str(args.config) == "/tmp/c.toml"


def test_rejects_unknown_type():
    with pytest.raises(SystemExit):
        build_parser().parse_args(["github.com", "BOGUS"])
