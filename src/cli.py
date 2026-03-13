import argparse
from enum import Enum

class Command(Enum):
    A="A"
    AAAA="AAAA"
    MX="MX"
    TXT="TXT"
    NS="NS"
    CNAME="CNAME"
    SOA="SOA"
    SRV="SRV"
    PTR="PTR"


parser=argparse.ArgumentParser(
    prog="Xdig",
    description="Demo Cli with subcommands",
    epilog="Text at the bottom of the help"

    )

parser.add_argument(
    "domain",
    nargs="*",
    help="One or more domains to resolve"
)

parser.add_argument(
    "record",
    choices=[c.value for c in Command],
    help="Type of DNS record to query" 
)

parser.add_argument(
    "-f",
    "--file",
    metavar="",
    help="File containing domains, one per line"
)


