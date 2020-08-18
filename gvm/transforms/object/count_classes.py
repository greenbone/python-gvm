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


@dataclass
class ResultCounter:
    """Counter class for the ResultCount class.

    Arguments:
        full: Total number of results.
        filtered: Number of results after filtering.
    """

    full: int
    filtered: int

    @staticmethod
    def resolve_result_counter(root: etree.Element) -> "ResultCounter":
        """ Resolve information about the number of results.

        Arguments:
            root: debug, hole, info, log, warning XML element from GMP.
        """
        full = get_int_from_element(root, "full")
        filtered = get_int_from_element(root, "filtered")

        return ResultCounter(full, filtered)


@dataclass
class ResultCount:
    """ Counts of results produced by scan.

    Arguments:
        current:
        full: Total number of results produced by scan.
        filtered: Number of results after filtering.
        debug: Number of "debug" results (threat level Debug).
        hole: Number of "hole" results (threat level High).
        info: Number of "info" results (threat level Low).
        log: Number of "log" results (threat level Log).
        warning: Number of "warning" results (threat level Medium).
        false_positive: Number of "false positive" results.
    """

    current: int
    full: int
    filtered: int
    debug: ResultCounter
    hole: ResultCounter
    info: ResultCounter
    log: ResultCounter
    warning: ResultCounter
    false_positive: ResultCounter

    @staticmethod
    def resolve_result_count(root: etree.Element):
        """ Resolve information of a result_count element from GMP.
        """
        current = get_int(root.text)
        full = get_int_from_element(root, "full")
        filtered = get_int_from_element(root, "filtered")
        debug = ResultCounter.resolve_result_counter(root.find("debug"))
        hole = ResultCounter.resolve_result_counter(root.find("hole"))
        info = ResultCounter.resolve_result_counter(root.find("info"))
        log = ResultCounter.resolve_result_counter(root.find("log"))
        warning = ResultCounter.resolve_result_counter(root.find("warning"))
        false_positiv = ResultCounter.resolve_result_counter(
            root.find("false_positive")
        )

        result_count = ResultCount(
            current,
            full,
            filtered,
            debug,
            hole,
            info,
            log,
            warning,
            false_positiv,
        )

        return result_count
