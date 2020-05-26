import datetime
from dataclasses import dataclass
from lxml import etree


@dataclass
class Owner:
    name: str


@dataclass
class Role:
    name: str


@dataclass
class PortCount:
    all: int
    tcp: int
    udp: int

@dataclass
class PortRange:
    port_range_id: str
    start: int
    end: int
    port_range_type: str
    comment: str

@dataclass
class PortList:
    port_list_id: str
    owner: Owner
    name: str
    comment: str
    creation_time: datetime
    modification_time: datetime
    writable: bool
    in_use: bool
    permissions: list
    port_count: PortCount
    port_ranges: list

@dataclass
class Permission: 
    name: str
