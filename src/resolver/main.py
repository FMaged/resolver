import logging
import sys

from .cli import build_parser
from .config import ConfigError, load_config
from .records import EmailDNSRecord
from .resolver import ResolverError, query_record

log = logging.getLogger(__name__)


def setup_logging(verbose: bool) -> None:
    logging.basicConfig(
        stream=sys.stderr,
        level=logging.DEBUG if verbose else logging.WARNING,
        format="%(levelname)s: %(message)s",
    )


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    setup_logging(args.verbose)

    try:
        config = load_config(args.config)
        answers = query_record(args.name, EmailDNSRecord(args.type), config)
    except (ConfigError, ResolverError) as e:
        log.error("%s", e)
        return 1

    if not answers:
        log.warning("no %s record for %s", args.type, args.name)
        return 0

    for answer in answers:
        print(answer.to_text())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
