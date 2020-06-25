from dataclasses import dataclass
from lxml import etree
from gvm.transforms.object.utils import get_bool_from_element
from .utils import (
    get_int_from_element,
    get_int,
)


@dataclass
class FamilyCount:
    """
    Arguments:
        current: The number of selected families.
        growing: Whether new families are automatically added.
    """

    current: int
    growing: bool

    @staticmethod
    def resolve_family_count(root: etree.Element) -> "FamilyCount":
        """ Resolve information of a family_count Element from GMP.

        :param root: family_count XML element from GMP.
        """
        if root is None:
            return None
        return FamilyCount(
            current=int(root.text),
            growing=get_bool_from_element(root, "growing"),
        )


@dataclass
class NvtCount:
    """
    Arguments:
        current: The number of selected NVTs.
        growing: Whether new NVTs are automatically added.
    """

    current: int
    growing: bool

    @staticmethod
    def resolve_nvt_count(root: etree.Element) -> "NvtCount":
        """ Resolve information of anvt_count Element from GMP.

        :param root: nvt_count XML element from GMP.
        """
        if root is None:
            return None
        return NvtCount(
            current=int(root.text),
            growing=get_bool_from_element(root, "growing"),
        )


@dataclass
class ReportCount:
    """
    Arguments:
        current: Number of reports.
        finished: Number of reports where the scan completed.
    """

    current: int
    finished: int

    @staticmethod
    def resolve_report_count(root: etree.Element) -> "ReportCount":
        """ Resolve information of a report_count Element from GMP.

        :param root: report_count XML element from GMP.
        """
        if root is None:
            return None
        return ReportCount(
            current=get_int(root.text),
            finished=get_int_from_element(root, "finished"),
        )
