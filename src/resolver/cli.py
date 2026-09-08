import argparse
from pathlib import Path

from .records import EmailDNSRecord


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="xdig",
        description="Look up DNS records for a domain",
    )

    parser.add_argument(
        "name",
        help="Domain name to resolve"
    )

    parser.add_argument(
        "type",
        nargs="?",
        choices=[r.value for r in EmailDNSRecord],
        default=EmailDNSRecord.A.value,
        help="DNS record type (default: A)"
    )

    parser.add_argument(
        "--config",
        type=Path,
        metavar="PATH",
        help="path to the config file"
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="show debug output on stderr"
    )

    return parser
