import logging
from ipaddress import IPv4Address

import dns.exception
import dns.resolver
from dns.rdata import Rdata

from .config import ResolverConfig
from .records import ARecord, EmailDNSRecord, HostName, MXRecord

log = logging.getLogger(__name__)


class ResolverError(Exception):
    pass


def _build_resolver(config: ResolverConfig) -> dns.resolver.Resolver:
    resolver = dns.resolver.Resolver()
    if config.dns_server is not None:
        resolver.nameservers = [str(config.dns_server)]
    resolver.lifetime = config.query_timeout
    # dnspython has no retry count; retries only toggles retrying on SERVFAIL
    resolver.retry_servfail = config.retries > 0
    return resolver


def query_record(
    domain_name: str,
    record_type: EmailDNSRecord,
    config: ResolverConfig | None = None,
) -> list[Rdata]:
    """Look up one record type. Returns [] when the domain has no such record."""
    resolver = _build_resolver(config or ResolverConfig())
    log.debug("querying %s %s", domain_name, record_type.value)

    try:
        return list(resolver.resolve(domain_name, record_type.value))
    except dns.resolver.NoAnswer:
        # Domain exists but has no record of this type
        return []
    except dns.resolver.NXDOMAIN as e:
        raise ResolverError(f"domain does not exist: {domain_name}") from e
    except dns.resolver.LifetimeTimeout as e:
        raise ResolverError(f"timed out querying {domain_name}") from e
    except dns.resolver.NoNameservers as e:
        raise ResolverError(f"no nameserver could answer for {domain_name}") from e
    except dns.exception.DNSException as e:
        raise ResolverError(f"DNS error for {domain_name} ({record_type.value}): {e}") from e


def get_mail_servers(
    domain_name: str, config: ResolverConfig | None = None
) -> list[MXRecord]:
    answers = query_record(domain_name, EmailDNSRecord.MX, config)

    servers = [
        MXRecord(
            priority=answer.preference,
            host=HostName(name=str(answer.exchange).rstrip(".")))
        for answer in answers
    ]
    return sorted(servers, key=lambda x: x.priority)


def get_mail_server_ipv4(
    mx_record: MXRecord, config: ResolverConfig | None = None
) -> ARecord:
    answers = query_record(mx_record.host.name, EmailDNSRecord.A, config)

    return ARecord(ips=[IPv4Address(answer.to_text()) for answer in answers])
