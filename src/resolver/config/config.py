from pathlib import Path
from pydantic import Field

from typing import Annotated, Literal
from ipaddress import IPv4Address
from enum import Enum

from records import Parent


class Protocol(str, Enum):
    UDP = "Udp"
    TCP = "Tcp"



class NetworkConfig(Parent):
    bind_address:IPv4Address
    dns_server: Annotated[IPv4Address, Field(alias="dns_ip")]
    port:Annotated[int, Field(gt=0, le=65535)]
    protocols: Protocol
    query_timeout: Annotated[int, Field(gt=0, lt=30)] 
    retries: Annotated[int, Field(gt=0, le=10)]
    max_concurrent_queries: Annotated[int, Field(gt=0, le=1000)]
    reuse_port: bool
    recursion: bool

    log_path: Path
    result_path:Path




def get_config(cfg_path:Path)->NetworkConfig:
    pass    

