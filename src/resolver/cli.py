import argparse
from enum import Enum

from records import EmailDNSRecord

parser=argparse.ArgumentParser(
    prog="Xdig",
    description="Demo Cli with subcommands",
    epilog="Text at the bottom of the help"

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
    help="DNS record type"
)



parser.add_argument(
    "-s",
    "--server",
    metavar="",
    help="DNS server"
)

parser.add_argument(
    "-f",
    "--file",
    metavar="",
    help="path to the file with domain names to resolve"
)


parser.add_argument(
    "--config",
    metavar="",
    help="path to the config"
)


parser.add_argument(
    "-4",
    action="store_true",
    help="use Ipv4 only"
)


parser.add_argument(
    "-6",
    action="store_true",
    help="use Ipv6 only"
)
