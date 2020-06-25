import datetime
from typing import List
from dataclasses import dataclass

from lxml import etree
from .user_classes import Owner, Permission

from .utils import (
    get_bool_from_element,
    get_text_from_element,
    get_datetime_from_element,
)


@dataclass
class PortCount:
    """
    Arguments:
        all: Total number of ports.
        tcp: Total number of TCP ports.
        udp: Total number of UDP ports.
    """

    all: int
    tcp: int
    udp: int

    @staticmethod
    def resolve_port_count(root: etree.Element) -> "PortCount":
        """
        Resolve information of a port_count Element from GMP.
        """
        if root is None:
            return None
        return PortCount(
            int(root.find("all").text),
            int(root.find("tcp").text),
            int(root.find("udp").text),
        )


@dataclass
class PortRange:
    """
    Arguments:
        uuid: uuid of the PortRange
        start: First port in range.
        end: Last port in range.
        port_range_type: The type of port: TCP, UDP, ....
        comment: The comment on the port range.
    """

    uuid: str
    start: int
    end: int
    port_range_type: str
    comment: str

    @staticmethod
    def resolve_port_ranges(root: etree.Element) -> List["PortRange"]:
        """
        resolve information of a port_ranges Element from GMP.
        """
        if root is None:
            return None
        port_ranges = []
        for port_range in root:
            port_ranges.append(
                PortRange(
                    port_range.get("id"),
                    int(port_range.find("start").text),
                    int(port_range.find("end").text),
                    port_range.find("type").text,
                    port_range.find("comment").text,
                )
            )
        return port_ranges


@dataclass
class PortList:
    """
    Arguments:
        uuid: uuid of the port list
        owner: Owner of the port list.
        name: The name of the port list.
        comment: The comment on the port list.
        creation_time: Date and time the port list was created.
        modification_time:  Date and time the port list was last modified.
        writable: Whether the port list is writable.
        in_use: Whether any targets are using the port list.
        permissions: Permissions that the current user has on the port list.
        port_count: Port count in port list.
        port_ranges: port ranges in port list.
    """

    uuid: str
    owner: Owner
    name: str
    comment: str
    creation_time: datetime.datetime
    modification_time: datetime.datetime
    writable: bool
    in_use: bool
    permissions: List[Permission]
    port_count: PortCount
    port_ranges: List[PortRange]

    @staticmethod
    def resolve_port_list(root: etree.Element) -> "PortList":
        """
        Resolve information from a port_list Element from GMP.
        """
        if root is None:
            return None
        uuid = root.get("id")
        owner = Owner.resolve_owner(root.find("owner"))
        name = get_text_from_element(root, "name")
        comment = get_text_from_element(root, "comment")

        creation_time = get_datetime_from_element(root, "creation_time")
        modification_time = get_datetime_from_element(root, "modification_time")

        writable = get_bool_from_element(root, "writable")
        in_use = get_bool_from_element(root, "in_use")

        permissions = Permission.resolve_permissions(root.find("permissions"))
        port_count = PortCount.resolve_port_count(root.find("port_count"))
        port_ranges = PortRange.resolve_port_ranges(root.find("port_ranges"))

        port_list = PortList(
            uuid,
            owner,
            name,
            comment,
            creation_time,
            modification_time,
            writable,
            in_use,
            permissions,
            port_count,
            port_ranges,
        )
        return port_list

    @staticmethod
    def resolve_port_lists(root: etree.Element) -> List["PortList"]:
        """ Resolve information of a port_lists Element from GMP.
        """
        result_list = []

        for child in root:
            if child.tag == "port_list":
                port_list = PortList.resolve_port_list(child)
                result_list.append(port_list)

        if len(result_list) == 1:
            return result_list[0]
        else:
            return result_list
