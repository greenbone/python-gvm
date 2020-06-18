import datetime

from dataclasses import dataclass
from lxml import etree
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
    name: str
    next_time: str
    trash: bool

    @staticmethod
    def resolve_schedule(root: etree.Element) -> "Schedule":
        name = get_text_from_element(root, "name")
        next_time = get_text_from_element(root, "next_time")
        trash = get_bool_from_element(root, "trash")

        schedule = Schedule(name, next_time, trash)
        return schedule


@dataclass
class ReportTask:
    uuid: str
    all_info_loaded: bool


@dataclass
class Severity:
    full: float
    filtered: float

    @staticmethod
    def resolve_severity(root: etree.Element):
        full = get_float_from_element(root, "full")
        filtered = get_float_from_element(root, "filtered")

        return Severity(full, filtered)


@dataclass
class Report:
    gmp: "Gmp"
    uuid: str
    format_id: str
    extension: str
    content_type: str
    owner: Owner
    name: str
    comment: str
    creation_time: datetime.datetime
    modification_time: datetime.datetime
    writable: bool
    in_use: bool
    gmp_version: str
    # sort
    # filters
    # severity_class
    scan_run_status: str
    # hosts
    # closed_cves
    # vulns
    # os
    # apps
    # ssl_certs
    # scan
    timestamp: datetime.datetime
    scan_start: datetime.datetime
    scan_end: datetime.datetime
    timezone: str
    timezone_abbrev: str
    # result_count
    severity: Severity
    # errors
    all_info_loaded: bool
    _task: "Task"

    @staticmethod
    def resolve_reports(root: etree.Element, gmp):
        reports = []
        for child in root:
            if child.tag == "report":
                reports.append(Report.resolve_report(child, gmp))
        if len(reports) == 1:
            return reports[0]
        return reports

    @staticmethod
    def resolve_report(root: etree.Element, gmp) -> "Report":
        if root is None:
            return None
        uuid = root.get("id")
        format_id = root.get("format_id")
        extension = root.get("extension")
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
            extension,
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

    def load_task(self, gmp) -> "Task":
        if self._task.uuid != "":
            if not self._task.all_info_loaded:
                self._task = gmp.get_task(self._task.uuid).tasks
                self._task.all_info_loaded = True

    @property
    def task(self) -> "Task":
        self.load_task(self.gmp)
        return self._task

    @task.setter
    def task(self, task: "Task"):
        self._task = task


@dataclass
class Nvt:
    oid: str
    name: str

    @staticmethod
    def resolve_nvt(root: etree.Element) -> "Nvt":
        if root is None:
            return None
        oid = root.get("oid")
        name = get_text_from_element(root, "name")

        nvt = Nvt(oid, name)

        return nvt


@dataclass
class Preference:
    nvt: Nvt
    preference_id: int
    hr_name: str
    name: str
    scanner_name: str
    preference_type: str
    value: str
    alternatives: list
    default: str

    @staticmethod
    def resolve_preferences(root: etree.Element) -> list:
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
        nvt = Nvt.resolve_nvt(root.find("nvt"))
        preference_id = get_int_from_element(root, "id")
        hr_name = get_text_from_element(root, "hr_name")
        name = get_text_from_element(root, "name")
        scanner_name = get_text_from_element(root, "scanner_name")
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
            scanner_name,
            preference_type,
            value,
            alternatives,
            default,
        )

        return preference


@dataclass
class TaskScanConfig:
    uuid: str
    trash: bool
    all_info_loaded: bool


@dataclass
class Task:
    gmp: "Gmp"
    uuid: str
    owner: Owner
    name: str
    comment: str
    creation_time: datetime.datetime
    modification_time: datetime.datetime
    writable: bool
    in_use: bool
    permissions: list
    user_tags: UserTags
    alterable: bool
    usage_type: str
    hosts_ordering: str

    # alert
    status: str
    progress: int
    report_count: ReportCount
    trend: str
    schedule: Schedule
    schedule_periods: int
    observers: Observers
    preferences: list
    all_info_loaded: bool
    _current_report: Report
    _last_report: Report
    _scan_config: TaskScanConfig
    _target: Target
    _scanner: Scanner

    @staticmethod
    def resolve_tasks(root: etree.Element, gmp) -> list:
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
        if self._current_report is None:
            return None

        if self._current_report.uuid != "":
            self._current_report = gmp.get_report(
                self._current_report.uuid
            ).reports
            self._current_report.all_info_loaded = True

    def load_last_report(self, gmp):
        if self._last_report is None:
            return None

        if self._last_report.uuid != "":
            self._last_report = gmp.get_report(self._last_report.uuid).reports
            self._last_report.all_info_loaded = True

    def load_scan_config(self, gmp):
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
        if self._target.uuid != "":
            if not self._target.all_info_loaded:
                trash = self._target.trash
                self._target = gmp.get_target(self._target.uuid).targets
                self._target.trash = trash
                self._target.all_info_loaded = True

    def load_scanner(self, gmp):
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
        self.load_current_report(self.gmp)
        return self._current_report

    @current_report.setter
    def current_report(self, report: Report):
        self._current_report = report

    @property
    def last_report(self) -> Report:
        self.load_last_report(self.gmp)
        return self._last_report

    @last_report.setter
    def last_report(self, report: Report):
        self._last_report = report

    @property
    def scan_config(self) -> "ScanConfig":
        self.load_scan_config(self.gmp)
        return self._scan_config

    @scan_config.setter
    def scan_config(self, scan_config: "ScanConfig"):
        self._scan_config = scan_config

    @property
    def target(self) -> Target:
        self.load_target(self.gmp)
        return self._target

    @target.setter
    def target(self, target: Target):
        self._target = target

    @property
    def scanner(self) -> Scanner:
        self.load_scanner(self.gmp)
        return self._scanner

    @scanner.setter
    def scanner(self, scanner: Scanner):
        self._scanner = scanner


@dataclass
class ScanConfig:
    uuid: str
    owner: Owner
    name: str
    comment: str
    creation_time: datetime.datetime
    modification_time: datetime.datetime
    writable: bool
    in_use: bool
    permissions: list
    family_count: FamilyCount
    nvt_count: NvtCount
    config_type: int
    usage_type: str
    max_nvt_count: int
    known_nvt_count: int
    scanner: Scanner
    user_tags: UserTags
    tasks: list
    # families
    # preferences
    # nvt_selectors
    trash: bool
    all_info_loaded: bool

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
            trash,
            False,
        )
