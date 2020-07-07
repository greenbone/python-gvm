import datetime
from typing import List
from dataclasses import dataclass
from lxml import etree
from gvm.protocols.base import GvmProtocol
from .user_classes import Owner, UserTags, Observers, Permission
from .count_classes import ReportCount, FamilyCount, NvtCount
from .scan_classes import Target, Scanner

from .utils import (
    get_bool_from_element,
    get_int_from_element,
    get_text_from_element,
    get_datetime_from_element,
    get_float_from_element,
    get_text,
)


@dataclass
class Schedule:
    """
    Arguments:
        name: The name of the schedule.
        next_time: The next date and time the schedule
            will be run in ISO format or "over"..
        trash: Whether the schedule is in the trashcan.
    """

    name: str
    next_time: str
    trash: bool

    @staticmethod
    def resolve_schedule(root: etree.Element) -> "Schedule":
        """ Resolve information of a 'schedule' element from GMP.
        """
        name = get_text_from_element(root, "name")
        next_time = get_text_from_element(root, "next_time")
        trash = get_bool_from_element(root, "trash")

        schedule = Schedule(name, next_time, trash)
        return schedule


@dataclass
class ReportTask:
    """ Helper Report, only with uuid, to load all information when needed.

    Arguments:
        uuid: uuid of the report.
        all_info_loaded: Whether all information is loaded.
    """

    uuid: str
    all_info_loaded: bool


@dataclass
class Severity:
    """
    Arguments:
        full: Maximum severity.
        filtered: Maximum severity after filtering.
    """

    full: float
    filtered: float

    @staticmethod
    def resolve_severity(root: etree.Element) -> "Severity":
        """ Resolve information of a 'severity' element from GMP.

        :param root: severity XML element from GMP.
        """
        full = get_float_from_element(root, "full")
        filtered = get_float_from_element(root, "filtered")

        return Severity(full, filtered)


@dataclass
class Report:
    """
    Arguments:
        gmp:
        uuid: uuid of the report.
        format_id:
        extension:
        content_type:
        owner: Owner of the report.
        name: Creation time as compatibility placeholder.
        comment: The comment on the report.
        creation_time: Date and time the report was created.
        modification_time: Date and time the report was last modified.
        writable: Whether the report is writable.
        in_use: Whether the report is in use.
        gmp_version: The GMP version.
        scan_run_status: Run status of task scan at time of report.
        timestamp: The time the scan was requested.
        scan_start: Start time of scan.
        scan_end: End time of scan.
        timezone: Name of timezone used for dates.
        timezone_abbrev: Abbreviation used for timezone.
        severity: Severity of the Report
        all_info_loaded: Whether all information is loaded.
        _task: The task the report belongs to.

    """

    gmp: GvmProtocol = None
    uuid: str = None
    format_id: str = None
    content_type: str = None
    owner: Owner = None
    name: str = None
    comment: str = None
    creation_time: datetime.datetime = None
    modification_time: datetime.datetime = None
    writable: bool = None
    in_use: bool = None
    gmp_version: str = None
    # sort
    # filters
    # severity_class
    scan_run_status: str = None
    # hosts
    # closed_cves
    # vulns
    # os
    # apps
    # ssl_certs
    # scan
    timestamp: datetime.datetime = None
    scan_start: datetime.datetime = None
    scan_end: datetime.datetime = None
    timezone: str = None
    timezone_abbrev: str = None
    # result_count = None
    severity: Severity = None
    # errors
    all_info_loaded: bool = False
    _task: ReportTask = None

    @staticmethod
    def resolve_reports(root: etree.Element, gmp) -> List["Report"]:
        """ Resolve information of a 'reports' element from GMP

        :param root: reports XML element from GMP.
        :param gmp: Gmp object, to automatically load more
            information when needed.
        """
        reports = []
        for child in root:
            if child.tag == "report":
                reports.append(Report.resolve_report(child, gmp))
        if len(reports) == 1:
            return reports[0]
        return reports

    @staticmethod
    def resolve_report(root: etree.Element, gmp) -> "Report":
        """ Resolve information of a 'report' element from GMP.

        :param root: report XML element from GMP.
        :param gmp: Gmp object, to automatically load more
            information when needed.
        """
        if root is None:
            return None
        uuid = root.get("id")
        format_id = root.get("format_id")
        content_type = root.get("content_type")
        owner = Owner.resolve_owner(root.find("owner"))
        name = get_text_from_element(root, "name")
        comment = get_text_from_element(root, "comment")
        creation_time = get_datetime_from_element(root, "creation_time")
        modification_time = get_datetime_from_element(root, "modification_time")
        writable = get_bool_from_element(root, "writable")
        in_use = get_bool_from_element(root, "in_use")
        task = root.find("task")
        if task is not None:
            task = ReportTask(task.get("id"), False)

        gmp_version = None
        # sort = None
        # filters = None
        # severity_class = None
        scan_run_status = None
        # hosts = None
        # closed_cves = None
        # vulns = None
        # os = None
        # apps = None
        # ssl_certs = None
        # scan  = None
        timestamp = None
        scan_start = None
        scan_end = None
        timezone = None
        timezone_abbrev = None
        # result_count = None
        severity = None
        # errors = None

        second_level = root.find("report")

        if second_level is not None:
            gmp_version = get_text_from_element(
                second_level.find("gmp"), "version"
            )
            # sort
            # filters
            # severity_class
            scan_run_status = get_text_from_element(
                second_level, "scan_run_status"
            )
            # hosts
            # closed_cves
            # vulns
            # os
            # apps
            # ssl_certs
            # scan
            timestamp = get_datetime_from_element(second_level, "timestamp")
            scan_start = get_datetime_from_element(second_level, "scan_start")
            scan_end = get_datetime_from_element(second_level, "scan_end")
            timezone = get_text_from_element(second_level, "timezone")
            timezone_abbrev = get_text_from_element(
                second_level, "timezone_abbrev"
            )
            # result_count
            severity = Severity.resolve_severity(second_level.find("severity"))
            # errors

        report = Report(
            gmp,
            uuid,
            format_id,
            content_type,
            owner,
            name,
            comment,
            creation_time,
            modification_time,
            writable,
            in_use,
            gmp_version,
            # sort,
            # filters,
            # severity_class,
            scan_run_status,
            # hosts,
            # closed_cves,
            # vulns,
            # os,
            # apps,
            # ssl_certs,
            # scan,
            timestamp,
            scan_start,
            scan_end,
            timezone,
            timezone_abbrev,
            # result_count,
            severity,
            # errors,
            False,
            task,
        )

        return report

    def load_task(self, gmp):
        """ Loads more information of the task, based on the uuid.
        """
        if self._task.uuid != "":
            # check if all information is already loaded
            if not self._task.all_info_loaded:
                self._task = gmp.get_task(self._task.uuid).tasks
                self._task.all_info_loaded = True

    @property
    def task(self) -> "Task":
        """Is called when the task is accessed.
        Loads more information of the task.
        """
        self.load_task(self.gmp)
        return self._task

    @task.setter
    def task(self, task: "Task"):
        """Setter for the task.
        """
        self._task = task


@dataclass
class Nvt:
    """
    Arguments:
        oid: oid of the NVT
        name: The name of the NVT.
    """

    oid: str
    name: str

    @staticmethod
    def resolve_nvt(root: etree.Element) -> "Nvt":
        """Resolve information of a 'nvt' element from GMP.

        :param root: nvt XML element from GMP.
        """
        if root is None:
            return None
        oid = root.get("oid")
        name = get_text_from_element(root, "name")

        nvt = Nvt(oid, name)

        return nvt


@dataclass
class Preference:
    """
    Arguments:
        nvt: NVT to which preference applies.
        preference_id: The ID of the preference.
        hr_name: The full, more "human readable" name of the preference.
        name: Full name of preference.
        scanner_name: Compact name of preference, from scanner.
        preference_type: The type of the preference.
        value: The value of the preference.
        alternatives: Alternative values for the preference.
        default: The default value of the preference.
    """

    nvt: Nvt
    preference_id: int
    hr_name: str
    name: str
    # scanner_name: str
    preference_type: str
    value: str
    alternatives: List[str]
    default: str

    @staticmethod
    def resolve_preferences(root: etree.Element) -> List["Preference"]:
        """ Resolve information of a 'preferences' element from GMP.

        :param root: preferences XML element from GMP.
        """
        if root is None:
            return None
        preferences = []
        for child in root:
            if child.tag == "preference":
                preferences.append(Preference.resolve_preference(child))
        if len(preferences) == 1:
            return preferences[0]
        return preferences

    @staticmethod
    def resolve_preference(root: etree.Element) -> "Preference":
        """ Resolve information of a 'preference' element from GMP.

        :param root: preference XML element from GMP.
        """
        nvt = Nvt.resolve_nvt(root.find("nvt"))
        preference_id = get_int_from_element(root, "id")
        hr_name = get_text_from_element(root, "hr_name")
        name = get_text_from_element(root, "name")
        # scanner_name = get_text_from_element(root, "scanner_name")
        preference_type = get_text_from_element(root, "type")
        value = get_text_from_element(root, "value")

        alternatives_xml = root.findall("alt")
        alternatives = []
        for alt in alternatives_xml:
            alternatives.append(get_text(alt))

        if len(alternatives) == 0:
            alternatives = None

        default = get_text_from_element(root, "default")

        preference = Preference(
            nvt,
            preference_id,
            hr_name,
            name,
            # scanner_name,
            preference_type,
            value,
            alternatives,
            default,
        )

        return preference


@dataclass
class TaskScanConfig:
    """ Helper scan config, only with uuid, to load all information when needed.

    Arguments:
        uuid: uuid of the scan config.
        trash: Whether the scan config is in the trash.
        all_info_loaded: Whether all information is loaded.
    """

    uuid: str
    trash: bool
    all_info_loaded: bool


@dataclass
class Task:
    """
    Arguments:
        gmp:
        uuid: uuid of the task
        owner: Owner of the task.
        name: The name of the task.
        comment: The comment on the task.
        creation_time: Creation time of the task.
        modification_time: Last time the task was modified.
        writable: Whether the task is writable.
        in_use: Whether this task is currently in use.
        permissions: Permissions that the current user has on the task.
        user_tags: Info on tags attached to the task.
        alterable: Whether the task is an Alterable Task.
        usage_type: The usage type of the task (scan or audit).
        hosts_ordering: The order hosts are scanned in.
        status: The run status of the task.
        progress: The percentage of the task that is complete.
        report_count: Number of reports.
        trend:
        schedule: When the task will run.
        schedule_periods: A limit to the number of times the task
            will be scheduled, or 0 for no limit.
        oberservers: Users, groups and roles allowed to observe this task.
        preferences: preferences of the task.
        all_info_loaded: Whether all information is loaded.
        _current_report:
        _last_report:
        _scan_config: The scan configuration used by the task.
        _target: The hosts scanned by the task.
        _scanner: The scanner used to scan the target.
    """

    gmp: GvmProtocol = None
    uuid: str = None
    owner: Owner = None
    name: str = None
    comment: str = None
    creation_time: datetime.datetime = None
    modification_time: datetime.datetime = None
    writable: bool = None
    in_use: bool = None
    permissions: list = None
    user_tags: UserTags = None
    alterable: bool = None
    usage_type: str = None
    hosts_ordering: str = None

    # alert
    status: str = None
    progress: int = None
    report_count: ReportCount = None
    trend: str = None
    schedule: Schedule = None
    schedule_periods: int = None
    observers: Observers = None
    preferences: list = None
    all_info_loaded: bool = None
    _current_report: Report = None
    _last_report: Report = None
    _scan_config: TaskScanConfig = None
    _target: Target = None
    _scanner: Scanner = None

    @staticmethod
    def resolve_tasks(root: etree.Element, gmp) -> List["Task"]:
        """ Resolve information of a 'tasks' element from GMP.

        :param root: tasks XML element from GMP.
        :param gmp: Gmp object, to automatically load more
            information when needed.
        """
        if root is None:
            return None

        tasks = []
        for child in root:
            if child.tag == "task":
                tasks.append(Task.resolve_task(child, gmp))
        if len(tasks) == 1:
            return tasks[0]
        else:
            return tasks

    @staticmethod
    def resolve_task(root: etree.Element, gmp) -> "Task":
        """ Resolve infromation from a 'task' element from GMP.

        :param root: task XML elemnt from GMP.
        :param gmp: Gmp object, to automatically load more
            information when needed.
        """
        uuid = root.get("id")
        owner = Owner.resolve_owner(root.find("owner"))
        name = root.find("name").text
        comment = get_text_from_element(root, "comment")

        creation_time = get_datetime_from_element(root, "creation_time")
        modification_time = get_datetime_from_element(root, "modification_time")

        writable = get_bool_from_element(root, "writable")
        in_use = get_bool_from_element(root, "in_use")

        permissions = Permission.resolve_permissions(root.find("permissions"))
        user_tags = UserTags.resolve_user_tags(root.find("user_tags"))

        alterable = get_bool_from_element(root, "alterable")
        usage_type = get_text_from_element(root, "usage_type")

        scan_config = root.find("config")
        if scan_config is not None:
            scan_config = TaskScanConfig(
                scan_config.get("id"),
                get_bool_from_element(scan_config, "trash"),
                False,
            )

        target = Target.resolve_target(root.find("target"), gmp)
        hosts_ordering = get_text_from_element(root, "hosts_ordering")
        scanner = Scanner.resolve_scanner(root.find("scanner"))
        status = get_text_from_element(root, "status")
        progress = get_int_from_element(root, "progress")

        report_count = ReportCount.resolve_report_count(
            root.find("report_count")
        )
        trend = get_text_from_element(root, "trend")

        schedule = Schedule.resolve_schedule(root.find("schedule"))
        schedule_periods = get_int_from_element(root, "schedule_periods")
        current_report = root.find("current_report")
        if current_report is not None:
            current_report = Report.resolve_report(
                current_report.find("report"), gmp
            )

        last_report = root.find("last_report")
        if last_report is not None:
            last_report = Report.resolve_report(last_report.find("report"), gmp)

        observers = Observers.resolve_observers(root.find("observers"), gmp)
        preferences = Preference.resolve_preferences(root.find("preferences"))

        task = Task(
            gmp,
            uuid,
            owner,
            name,
            comment,
            creation_time,
            modification_time,
            writable,
            in_use,
            permissions,
            user_tags,
            alterable,
            usage_type,
            hosts_ordering,
            status,
            progress,
            report_count,
            trend,
            schedule,
            schedule_periods,
            observers,
            preferences,
            False,
            current_report,
            last_report,
            scan_config,
            target,
            scanner,
        )

        return task

    def load_current_report(self, gmp):
        """ Loads more information of the current report, based on the uuid.
        """
        if self._current_report is None:
            return None

        if self._current_report.uuid != "":
            if not self._current_report.all_info_loaded:
                self._current_report = gmp.get_report(
                    self._current_report.uuid
                ).reports
                self._current_report.all_info_loaded = True

    def load_last_report(self, gmp):
        """ Loads more information of the last report, based on the uuid.
        """
        if self._last_report is None:
            return None

        if self._last_report.uuid != "":
            if not self._last_report.all_info_loaded:
                self._last_report = gmp.get_report(
                    self._last_report.uuid
                ).reports
                self._last_report.all_info_loaded = True

    def load_scan_config(self, gmp):
        """ Loads more information of the scan config, based on the uuid.
        """
        if self._scan_config is None:
            return None

        if self._scan_config.uuid != "":
            if not self._scan_config.all_info_loaded:
                trash = self._scan_config.trash
                self._scan_config = gmp.get_config(
                    self._scan_config.uuid
                ).scan_configs
                self._scan_config.trash = trash
                self._scan_config.all_info_loaded = True

    def load_target(self, gmp):
        """ Loads more information of the target, based on the uuid.
        """
        if self._target is None:
            return None

        if self._target.uuid != "":
            if not self._target.all_info_loaded:
                trash = self._target.trash
                self._target = gmp.get_target(self._target.uuid).targets
                self._target.trash = trash
                self._target.all_info_loaded = True

    def load_scanner(self, gmp):
        """ Loads more information of the scanner, based on the uuid.
        """
        if self._scanner is None:
            return None

        # das Abfragen von Informationen zu einem Scanner dauert sehr lange.
        if self._scanner.uuid != "":
            if not self._scanner.all_info_loaded:
                # safe this information, because it's always None in get_scanner
                trash = self._scanner.trash
                self._scanner = gmp.get_scanner(self._scanner.uuid).scanners
                self._scanner.trash = trash
                self._scanner.all_info_loaded = True

    # Load additional Information when needed
    @property
    def current_report(self) -> Report:
        """
        Is called when the current report is accessed.
        Loads more information of the current report.
        """
        self.load_current_report(self.gmp)
        return self._current_report

    @current_report.setter
    def current_report(self, report: Report):
        self._current_report = report

    @property
    def last_report(self) -> Report:
        """
        Is called when the last report is accessed.
        Loads more information of the last report.
        """
        self.load_last_report(self.gmp)
        return self._last_report

    @last_report.setter
    def last_report(self, report: Report):
        self._last_report = report

    @property
    def scan_config(self) -> "ScanConfig":
        """
        Is called when the scan config is accessed.
        Loads more information of the scan config.
        """
        self.load_scan_config(self.gmp)
        return self._scan_config

    @scan_config.setter
    def scan_config(self, scan_config: "ScanConfig"):
        self._scan_config = scan_config

    @property
    def target(self) -> Target:
        """
        Is called when the target is accessed.
        Loads more information of the target.
        """
        self.load_target(self.gmp)
        return self._target

    @target.setter
    def target(self, target: Target):
        self._target = target

    @property
    def scanner(self) -> Scanner:
        """
        Is called when the scanner is accessed.
        Loads more information of the scanner.
        """
        self.load_scanner(self.gmp)
        return self._scanner

    @scanner.setter
    def scanner(self, scanner: Scanner):
        self._scanner = scanner


@dataclass
class ScanConfig:
    uuid: str = None
    owner: Owner = None
    name: str = None
    comment: str = None
    creation_time: datetime.datetime = None
    modification_time: datetime.datetime = None
    writable: bool = None
    in_use: bool = None
    permissions: list = None
    family_count: FamilyCount = None
    nvt_count: NvtCount = None
    config_type: int = None
    usage_type: str = None
    max_nvt_count: int = None
    known_nvt_count: int = None
    scanner: Scanner = None
    user_tags: UserTags = None
    tasks: List[Task] = None
    # families
    preferences: List[Preference] = None
    # nvt_selectors
    trash: bool = None
    all_info_loaded: bool = False

    @staticmethod
    def resolve_configs(root: etree.Element, gmp) -> list:
        configs = []
        for child in root:
            if child.tag == "config":
                configs.append(ScanConfig.resolve_config(child, gmp))

        if len(configs) == 1:
            return configs[0]
        else:
            return configs

    @staticmethod
    def resolve_config(root: etree.Element, gmp) -> "ScanConfig":
        if root is None:
            return None
        uuid = root.get("id")
        owner = Owner.resolve_owner(root.find("owner"))
        name = root.find("name").text
        comment = get_text_from_element(root, "comment")

        creation_time = get_datetime_from_element(root, "creation_time")
        modification_time = get_datetime_from_element(root, "modification_time")

        writable = get_bool_from_element(root, "writable")
        in_use = get_bool_from_element(root, "in_use")

        permissions = Permission.resolve_permissions(root.find("permissions"))
        family_count = FamilyCount.resolve_family_count(
            root.find("family_count")
        )
        nvt_count = NvtCount.resolve_nvt_count(root.find("nvt_count"))
        config_type = get_int_from_element(root, "type")
        usage_type = get_text_from_element(root, "usage_type")
        max_nvt_count = get_int_from_element(root, "max_nvt_count")
        known_nvt_count = get_int_from_element(root, "known_nvt_count")
        scanner = Scanner.resolve_scanner(root.find("scanner"))
        user_tags = UserTags.resolve_user_tags(root.find("user_tags"))
        tasks = Task.resolve_tasks(root.find("tasks"), gmp)
        preferences = Preference.resolve_preferences(root.find("preferences"))

        trash = get_bool_from_element(root, "trash")

        return ScanConfig(
            uuid,
            owner,
            name,
            comment,
            creation_time,
            modification_time,
            writable,
            in_use,
            permissions,
            family_count,
            nvt_count,
            config_type,
            usage_type,
            max_nvt_count,
            known_nvt_count,
            scanner,
            user_tags,
            tasks,
            preferences,
            trash,
            False,
        )
