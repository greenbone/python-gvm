from dataclasses import dataclass
from lxml import etree
from .utils import (
    get_int_from_element,
    get_int,
)


@dataclass
class FamilyCount:
    current: int
    growing: int

    @staticmethod
    def resolve_family_count(root: etree.Element) -> "FamilyCount":
        if root is None:
            return None
        return FamilyCount(
            current=int(root.text), growing=int(root.find("growing").text)
        )


@dataclass
class NvtCount:
    current: int
    growing: int

    @staticmethod
    def resolve_nvt_count(root: etree.Element) -> "NvtCount":
        if root is None:
            return None
        return NvtCount(
            current=int(root.text), growing=int(root.find("growing").text)
        )


@dataclass
class ReportCount:
    current: int
    finished: int

    @staticmethod
    def resolve_report_count(root: etree.Element) -> "ReportCount":
        if root is None:
            return None
        return ReportCount(
            current=get_int(root.text),
            finished=get_int_from_element(root, "finished"),
        )
