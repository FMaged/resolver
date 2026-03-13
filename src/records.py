from pydantic import BaseModel, ConfigDict, Field, model_validator

from ipaddress import IPv4Address, IPv6Address
from typing import Annotated


class Parent(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        str_to_lower=False,
        frozen=True,
    
    )

class HostName(Parent):
    name:Annotated[
        str,
        Field(
            min_length=1,
            max_length=254,
            pattern=r"^([a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,63}\.?$"
        )
    ]

class ARecord(Parent):
    ips: Annotated[list[IPv4Address],Field(min_length=1)]


class AAAARecord(Parent):
    ip: Annotated[list[IPv6Address], Field(min_length=1)]



class MXRecord(Parent):
    priority: Annotated[int, Field(ge=0,le=65535)]
    host: HostName


class CNAMERecord(Parent):
    target: HostName

class NSRecord(Parent):
    name_server: HostName

class TXTRecord(Parent):
    text: Annotated[list[Annotated[str, Field(max_length=255)]], Field(min_length=1)]

    @model_validator(mode="after")
    def validate_txt(self):
        if sum(len(s.encode()) for s in self.text) > 65535:
            raise ValueError("TXT record exceeds 65535 bytes total")
        return self


class PTRRecord(Parent):
    host: HostName

class SOARecord(Parent):
    mname: HostName
    rname: HostName
    serial: Annotated[int, Field(ge=0)]
    refresh: Annotated[int, Field(ge=0)]
    retry: Annotated[int, Field(ge=0)]
    expire: Annotated[int, Field(ge=0)]
    minimum: Annotated[int, Field(ge=0)]