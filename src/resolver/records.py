from enum import Enum
from ipaddress import IPv4Address, IPv6Address
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, model_validator


class EmailDNSRecord(str, Enum):
    ANY="ANY"
    A="A"
    AAAA="AAAA"
    MX = "MX"
    CNAME="CNAME"
    NS="NS"
    PTR="PTR"
    TXT="TXT"
    SOA="SOA"
    SPF="SPF"

class Base(BaseModel):
    # forbid: an unknown key in config.toml should fail loudly, not be ignored
    model_config = ConfigDict(
        extra='forbid',
        str_to_lower=False,
        frozen=True,
    )

class HostName(Base):
    name:Annotated[
        str,
        Field(
            min_length=1,
            max_length=254,
            pattern=r"^([a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,63}\.?$"
        )
    ]

class ARecord(Base):
    ips: Annotated[list[IPv4Address],Field(min_length=1)]


class AAAARecord(Base):
    ips: Annotated[list[IPv6Address], Field(min_length=1)]



class MXRecord(Base):
    priority: Annotated[int, Field(ge=0,le=65535)]
    host: HostName


class CNAMERecord(Base):
    target: HostName

class NSRecord(Base):
    name_server: HostName

class TXTRecord(Base):
    text: Annotated[list[Annotated[str, Field(max_length=255)]], Field(min_length=1)]

    @model_validator(mode="after")
    def validate_txt(self):
        if sum(len(s.encode()) for s in self.text) > 65535:
            raise ValueError("TXT record exceeds 65535 bytes total")
        return self


class PTRRecord(Base):
    host: HostName

class SOARecord(Base):
    mname: HostName
    rname: HostName
    serial: Annotated[int, Field(ge=0)]
    refresh: Annotated[int, Field(ge=0)]
    retry: Annotated[int, Field(ge=0)]
    expire: Annotated[int, Field(ge=0)]
    minimum: Annotated[int, Field(ge=0)]
