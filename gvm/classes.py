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
class PortList:
    id: str
    owner: Owner
    name: str
    comment: str
    creation_time: datetime
    modification_time: datetime
    writable: bool
    in_use: bool
    permissions: list
    # port_count: int
    # port_ranges: list


class Permission:
    name: str
