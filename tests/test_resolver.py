import dns.resolver
import pytest

from resolver.config import ResolverConfig
from resolver.records import EmailDNSRecord
from resolver.resolver import ResolverError, get_mail_servers, query_record


class FakeMX:
    def __init__(self, preference, exchange):
        self.preference = preference
        self.exchange = exchange


def patch_resolve(monkeypatch, result):
    """Make Resolver.resolve return `result`, or raise it if it is an exception."""
    def fake_resolve(self, *args, **kwargs):
        if isinstance(result, Exception):
            raise result
        return result

    monkeypatch.setattr(dns.resolver.Resolver, "resolve", fake_resolve)


def test_mail_servers_sorted_by_priority(monkeypatch):
    patch_resolve(monkeypatch, [
        FakeMX(20, "alt.example.com."),
        FakeMX(5, "primary.example.com."),
    ])

    servers = get_mail_servers("example.com")

    assert [s.priority for s in servers] == [5, 20]
    # trailing dot stripped by get_mail_servers
    assert servers[0].host.name == "primary.example.com"


def test_no_answer_returns_empty(monkeypatch):
    patch_resolve(monkeypatch, dns.resolver.NoAnswer())
    assert query_record("example.com", EmailDNSRecord.MX) == []


def test_nxdomain_raises(monkeypatch):
    patch_resolve(monkeypatch, dns.resolver.NXDOMAIN())
    with pytest.raises(ResolverError, match="does not exist"):
        query_record("nope.invalid", EmailDNSRecord.A)


def test_no_nameservers_raises(monkeypatch):
    patch_resolve(monkeypatch, dns.resolver.NoNameservers())
    with pytest.raises(ResolverError, match="no nameserver"):
        query_record("example.com", EmailDNSRecord.A)


def test_config_applied_to_resolver(monkeypatch):
    seen = {}

    def fake_resolve(self, *args, **kwargs):
        seen["nameservers"] = self.nameservers
        seen["lifetime"] = self.lifetime
        return []

    monkeypatch.setattr(dns.resolver.Resolver, "resolve", fake_resolve)
    config = ResolverConfig(dns_server="9.9.9.9", query_timeout=2)
    query_record("example.com", EmailDNSRecord.A, config)

    assert seen["nameservers"] == ["9.9.9.9"]
    assert seen["lifetime"] == 2
