# -*- coding: utf-8 -*-
# Copyright (C) 2018 - 2020 Greenbone Networks GmbH
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# pylint: disable=arguments-differ, redefined-builtin, too-many-lines

"""
Module for communication with gvmd in `Greenbone Management Protocol version 9`_

.. _Greenbone Management Protocol version 9:
    https://docs.greenbone.net/API/GMP/gmp-9.0.html
"""
import collections
import numbers

from typing import Any, List, Optional, Callable

from gvm.errors import InvalidArgument, InvalidArgumentType, RequiredArgument
from gvm.utils import deprecation
from gvm.xml import XmlCommand

from gvm.protocols.base import GvmProtocol
from gvm.connections import GvmConnection
from gvm.protocols.gmpv7.gmpv7 import (
    _to_bool,
    _add_filter,
    _is_list_like,
    _to_comma_list,
)

from . import types
from .types import *  # pylint: disable=unused-wildcard-import, wildcard-import
from .types import _UsageType as UsageType

_EMPTY_POLICY_ID = '085569ce-73ed-11df-83c3-002264764cea'


def _check_event(
    event: AlertEvent, condition: AlertCondition, method: AlertMethod
):
    if event == AlertEvent.TASK_RUN_STATUS_CHANGED:
        if not condition:
            raise RequiredArgument(
                "condition is required for event {}".format(event.name)
            )

        if not method:
            raise RequiredArgument(
                "method is required for event {}".format(event.name)
            )

        if condition not in (
            AlertCondition.ALWAYS,
            AlertCondition.FILTER_COUNT_CHANGED,
            AlertCondition.FILTER_COUNT_AT_LEAST,
            AlertCondition.SEVERITY_AT_LEAST,
            AlertCondition.SEVERITY_CHANGED,
        ):
            raise InvalidArgument(
                "Invalid condition {} for event {}".format(
                    condition.name, event.name
                )
            )
    elif event in (
        AlertEvent.NEW_SECINFO_ARRIVED,
        AlertEvent.UPDATED_SECINFO_ARRIVED,
    ):
        if not condition:
            raise RequiredArgument(
                "condition is required for event {}".format(event.name)
            )

        if not method:
            raise RequiredArgument(
                "method is required for event {}".format(event.name)
            )

        if condition != AlertCondition.ALWAYS:
            raise InvalidArgument(
                "Invalid condition {} for event {}".format(
                    condition.name, event.name
                )
            )
        if method not in (
            AlertMethod.SCP,
            AlertMethod.SEND,
            AlertMethod.SMB,
            AlertMethod.SNMP,
            AlertMethod.SYSLOG,
            AlertMethod.EMAIL,
        ):
            raise InvalidArgument(
                "Invalid method {} for event {}".format(method.name, event.name)
            )
    elif event in (
        AlertEvent.TICKET_RECEIVED,
        AlertEvent.OWNED_TICKET_CHANGED,
        AlertEvent.ASSIGNED_TICKET_CHANGED,
    ):
        if not condition:
            raise RequiredArgument(
                "condition is required for event {}".format(event.name)
            )

        if not method:
            raise RequiredArgument(
                "method is required for event {}".format(event.name)
            )
        if condition != AlertCondition.ALWAYS:
            raise InvalidArgument(
                "Invalid condition {} for event {}".format(
                    condition.name, event.name
                )
            )
        if method not in (
            AlertMethod.EMAIL,
            AlertMethod.START_TASK,
            AlertMethod.SYSLOG,
        ):
            raise InvalidArgument(
                "Invalid method {} for event {}".format(method.name, event.name)
            )
    elif event is not None:
        raise InvalidArgument('Invalid event "{}"'.format(event.name))


class GmpV9Mixin(GvmProtocol):

    types = types

    def __init__(
        self,
        connection: GvmConnection,
        *,
        transform: Optional[Callable[[str], Any]] = None
    ):
        super().__init__(connection, transform=transform)

        # Is authenticated on gvmd
        self._authenticated = False

    def create_alert(
        self,
        name: str,
        condition: AlertCondition,
        event: AlertEvent,
        method: AlertMethod,
        *,
        method_data: Optional[dict] = None,
        event_data: Optional[dict] = None,
        condition_data: Optional[dict] = None,
        filter_id: Optional[int] = None,
        comment: Optional[str] = None
    ) -> Any:
        """Create a new alert

        Arguments:
            name: Name of the new Alert
            condition: The condition that must be satisfied for the alert
                to occur; if the event is either 'Updated SecInfo arrived' or
                'New SecInfo arrived', condition must be 'Always'. Otherwise,
                condition can also be on of 'Severity at least', 'Filter count
                changed' or 'Filter count at least'.
            event: The event that must happen for the alert to occur, one
                of 'Task run status changed', 'Updated SecInfo arrived' or 'New
                SecInfo arrived'
            method: The method by which the user is alerted, one of 'SCP',
                'Send', 'SMB', 'SNMP', 'Syslog' or 'Email'; if the event is
                neither 'Updated SecInfo arrived' nor 'New SecInfo arrived',
                method can also be one of 'Start Task', 'HTTP Get', 'Sourcefire
                Connector' or 'verinice Connector'.
            condition_data: Data that defines the condition
            event_data: Data that defines the event
            method_data: Data that defines the method
            filter_id: Filter to apply when executing alert
            comment: Comment for the alert

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument(
                function=self.create_alert.__name__, argument='name'
            )

        if not condition:
            raise RequiredArgument(
                function=self.create_alert.__name__, argument='condition'
            )

        if not event:
            raise RequiredArgument(
                function=self.create_alert.__name__, argument='event'
            )

        if not method:
            raise RequiredArgument(
                function=self.create_alert.__name__, argument='method'
            )

        if not isinstance(condition, AlertCondition):
            raise InvalidArgumentType(
                function=self.create_alert.__name__,
                argument='condition',
                arg_type=AlertCondition.__name__,
            )

        if not isinstance(event, AlertEvent):
            raise InvalidArgumentType(
                function=self.create_alert.__name__,
                argument='even',
                arg_type=AlertEvent.__name__,
            )

        if not isinstance(method, AlertMethod):
            raise InvalidArgumentType(
                function=self.create_alert.__name__,
                argument='method',
                arg_type=AlertMethod.__name__,
            )

        _check_event(event, condition, method)

        cmd = XmlCommand("create_alert")
        cmd.add_element("name", name)

        conditions = cmd.add_element("condition", condition.value)

        if condition_data is not None:
            for key, value in condition_data.items():
                _data = conditions.add_element("data", value)
                _data.add_element("name", key)

        events = cmd.add_element("event", event.value)

        if event_data is not None:
            for key, value in event_data.items():
                _data = events.add_element("data", value)
                _data.add_element("name", key)

        methods = cmd.add_element("method", method.value)

        if method_data is not None:
            for key, value in method_data.items():
                _data = methods.add_element("data", value)
                _data.add_element("name", key)

        if filter_id:
            cmd.add_element("filter", attrs={"id": filter_id})

        if comment:
            cmd.add_element("comment", comment)

        return self._send_xml_command(cmd)

    def create_audit(
        self,
        name: str,
        policy_id: str,
        target_id: str,
        scanner_id: str,
        *,
        alterable: Optional[bool] = None,
        hosts_ordering: Optional[HostsOrdering] = None,
        schedule_id: Optional[str] = None,
        alert_ids: Optional[List[str]] = None,
        comment: Optional[str] = None,
        schedule_periods: Optional[int] = None,
        observers: Optional[List[str]] = None,
        preferences: Optional[dict] = None
    ) -> Any:
        """Create a new audit task

        Arguments:
            name: Name of the new audit
            policy_id: UUID of policy to use by the audit
            target_id: UUID of target to be scanned
            scanner_id: UUID of scanner to use for scanning the target
            comment: Comment for the audit
            alterable: Whether the task should be alterable
            alert_ids: List of UUIDs for alerts to be applied to the audit
            hosts_ordering: The order hosts are scanned in
            schedule_id: UUID of a schedule when the audit should be run.
            schedule_periods: A limit to the number of times the audit will be
                scheduled, or 0 for no limit
            observers: List of names or ids of users which should be allowed to
                observe this audit
            preferences: Name/Value pairs of scanner preferences.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """

        return self.__create_task(
            name=name,
            config_id=policy_id,
            target_id=target_id,
            scanner_id=scanner_id,
            usage_type=UsageType.AUDIT,
            function=self.create_audit.__name__,
            alterable=alterable,
            hosts_ordering=hosts_ordering,
            schedule_id=schedule_id,
            alert_ids=alert_ids,
            comment=comment,
            schedule_periods=schedule_periods,
            observers=observers,
            preferences=preferences,
        )

    def create_config(
        self, config_id: str, name: str, *, comment: Optional[str] = None
    ) -> Any:
        """Create a new scan config

        Arguments:
            config_id: UUID of the existing scan config
            name: Name of the new scan config
            comment: A comment on the config

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        return self.__create_config(
            config_id=config_id,
            name=name,
            comment=comment,
            usage_type=UsageType.SCAN,
            function=self.create_config.__name__,
        )

    def create_config_from_osp_scanner(
        self, scanner_id: str, name: str, *, comment: Optional[str] = None
    ) -> Any:
        """Create a new scan config from an ospd scanner.

        Create config by retrieving the expected preferences from the given
        scanner via OSP.

        Arguments:
            scanner_id: UUID of an OSP scanner to get config data from
            name: Name of the new scan config
            comment: A comment on the config

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        return self.__create_config_from_osp_scanner(
            scanner_id=scanner_id,
            name=name,
            comment=comment,
            usage_type=UsageType.SCAN,
            function=self.create_config.__name__,
        )

    def create_policy(
        self, name: str, *, policy_id: str = None, comment: Optional[str] = None
    ) -> Any:
        """Create a new policy config

        Arguments:
            name: Name of the new policy
            policy_id: UUID of an existing policy as base. By default the empty
                policy is used.
            comment: A comment on the policy

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if policy_id is None:
            policy_id = _EMPTY_POLICY_ID
        return self.__create_config(
            config_id=policy_id,
            name=name,
            comment=comment,
            usage_type=UsageType.POLICY,
            function=self.create_policy.__name__,
        )

    def create_task(
        self,
        name: str,
        config_id: str,
        target_id: str,
        scanner_id: str,
        *,
        alterable: Optional[bool] = None,
        hosts_ordering: Optional[HostsOrdering] = None,
        schedule_id: Optional[str] = None,
        alert_ids: Optional[List[str]] = None,
        comment: Optional[str] = None,
        schedule_periods: Optional[int] = None,
        observers: Optional[List[str]] = None,
        preferences: Optional[dict] = None
    ) -> Any:
        """Create a new scan task

        Arguments:
            name: Name of the task
            config_id: UUID of scan config to use by the task
            target_id: UUID of target to be scanned
            scanner_id: UUID of scanner to use for scanning the target
            comment: Comment for the task
            alterable: Whether the task should be alterable
            alert_ids: List of UUIDs for alerts to be applied to the task
            hosts_ordering: The order hosts are scanned in
            schedule_id: UUID of a schedule when the task should be run.
            schedule_periods: A limit to the number of times the task will be
                scheduled, or 0 for no limit
            observers: List of names or ids of users which should be allowed to
                observe this task
            preferences: Name/Value pairs of scanner preferences.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        return self.__create_task(
            name=name,
            config_id=config_id,
            target_id=target_id,
            scanner_id=scanner_id,
            usage_type=UsageType.SCAN,
            function=self.create_task.__name__,
            alterable=alterable,
            hosts_ordering=hosts_ordering,
            schedule_id=schedule_id,
            alert_ids=alert_ids,
            comment=comment,
            schedule_periods=schedule_periods,
            observers=observers,
            preferences=preferences,
        )

    def create_tls_certificate(
        self,
        name: str,
        certificate: str,
        *,
        comment: Optional[str] = None,
        trust: Optional[bool] = None
    ) -> Any:
        """Create a new TLS certificate

        Arguments:
            name: Name of the TLS certificate, defaulting to the MD5
                fingerprint.
            certificate: The Base64 encoded certificate data (x.509 DER or PEM).
            comment: Comment for the TLS certificate.
            trust: Whether the certificate is trusted.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument(
                function=self.create_tls_certificate.__name__, argument='name'
            )
        if not certificate:
            raise RequiredArgument(
                function=self.create_tls_certificate.__name__,
                argument='certificate',
            )

        cmd = XmlCommand("create_tls_certificate")

        if comment:
            cmd.add_element("comment", comment)

        cmd.add_element("name", name)
        cmd.add_element("certificate", certificate)

        if trust:
            cmd.add_element("trust", _to_bool(trust))

        return self._send_xml_command(cmd)

    def get_tls_certificates(
        self,
        *,
        filter: Optional[str] = None,
        filter_id: Optional[str] = None,
        include_certificate_data: Optional[bool] = None,
        details: Optional[bool] = None
    ) -> Any:
        """Request a list of TLS certificates

        Arguments:
            filter: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            include_certificate_data: Whether to include the certificate data in
                the response

        Returns:
            The response. See :py:meth:`send_command` for details.
        """

        cmd = XmlCommand("get_tls_certificates")

        _add_filter(cmd, filter, filter_id)

        if details is not None:
            cmd.set_attribute("details", _to_bool(details))

        if include_certificate_data is not None:
            cmd.set_attribute(
                "include_certificate_data", _to_bool(include_certificate_data)
            )

        return self._send_xml_command(cmd)

    def get_tls_certificate(self, tls_certificate_id: str) -> Any:
        """Request a single TLS certificate

        Arguments:
            tls_certificate_id: UUID of an existing TLS certificate

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_tls_certificates")

        if not tls_certificate_id:
            raise RequiredArgument(
                function=self.get_tls_certificate.__name__,
                argument='tls_certificate_id',
            )

        cmd.set_attribute("tls_certificate_id", tls_certificate_id)

        # for single tls certificate always request cert data
        cmd.set_attribute("include_certificate_data", "1")

        # for single entity always request all details
        cmd.set_attribute("details", "1")

        return self._send_xml_command(cmd)

    def modify_alert(
        self,
        alert_id: str,
        *,
        name: Optional[str] = None,
        comment: Optional[str] = None,
        filter_id: Optional[str] = None,
        event: Optional[AlertEvent] = None,
        event_data: Optional[dict] = None,
        condition: Optional[AlertCondition] = None,
        condition_data: Optional[dict] = None,
        method: Optional[AlertMethod] = None,
        method_data: Optional[dict] = None
    ) -> Any:
        """Modifies an existing alert.

        Arguments:
            alert_id: UUID of the alert to be modified.
            name: Name of the Alert.
            condition: The condition that must be satisfied for the alert to
                occur. If the event is either 'Updated SecInfo
                arrived' or 'New SecInfo arrived', condition must be 'Always'.
                Otherwise, condition can also be on of 'Severity at least',
                'Filter count changed' or 'Filter count at least'.
            condition_data: Data that defines the condition
            event: The event that must happen for the alert to occur, one of
                'Task run status changed', 'Updated SecInfo arrived' or
                'New SecInfo arrived'
            event_data: Data that defines the event
            method: The method by which the user is alerted, one of 'SCP',
                'Send', 'SMB', 'SNMP', 'Syslog' or 'Email';
                if the event is neither 'Updated SecInfo arrived' nor
                'New SecInfo arrived', method can also be one of 'Start Task',
                'HTTP Get', 'Sourcefire Connector' or 'verinice Connector'.
            method_data: Data that defines the method
            filter_id: Filter to apply when executing alert
            comment: Comment for the alert

        Returns:
            The response. See :py:meth:`send_command` for details.
        """

        if not alert_id:
            raise RequiredArgument(
                function=self.modify_alert.__name__, argument='alert_id'
            )

        cmd = XmlCommand("modify_alert")
        cmd.set_attribute("alert_id", str(alert_id))

        if name:
            cmd.add_element("name", name)

        if comment:
            cmd.add_element("comment", comment)

        if filter_id:
            cmd.add_element("filter", attrs={"id": filter_id})

        if condition:
            if not isinstance(condition, AlertCondition):
                raise InvalidArgumentType(
                    function=self.modify_alert.__name__,
                    argument='condition',
                    arg_type=AlertCondition.__name__,
                )

            conditions = cmd.add_element("condition", condition.value)

            if condition_data is not None:
                for key, value in condition_data.items():
                    _data = conditions.add_element("data", value)
                    _data.add_element("name", key)

        if method:
            if not isinstance(method, AlertMethod):
                raise InvalidArgumentType(
                    function=self.modify_alert.__name__,
                    argument='method',
                    arg_type=AlertMethod.__name__,
                )

            methods = cmd.add_element("method", method.value)

            if method_data is not None:
                for key, value in method_data.items():
                    _data = methods.add_element("data", value)
                    _data.add_element("name", key)

        if event:
            if not isinstance(event, AlertEvent):
                raise InvalidArgumentType(
                    function=self.modify_alert.__name__,
                    argument='event',
                    arg_type=AlertEvent.__name__,
                )

            _check_event(event, condition, method)

            events = cmd.add_element("event", event.value)

            if event_data is not None:
                for key, value in event_data.items():
                    _data = events.add_element("data", value)
                    _data.add_element("name", key)

        return self._send_xml_command(cmd)

    def modify_audit(
        self,
        audit_id: str,
        *,
        name: Optional[str] = None,
        policy_id: Optional[str] = None,
        target_id: Optional[str] = None,
        scanner_id: Optional[str] = None,
        alterable: Optional[bool] = None,
        hosts_ordering: Optional[HostsOrdering] = None,
        schedule_id: Optional[str] = None,
        schedule_periods: Optional[int] = None,
        comment: Optional[str] = None,
        alert_ids: Optional[List[str]] = None,
        observers: Optional[List[str]] = None,
        preferences: Optional[dict] = None
    ) -> Any:
        """Modifies an existing task.

        Arguments:
            audit_id: UUID of audit to modify.
            name: The name of the audit.
            policy_id: UUID of policy to use by the audit
            target_id: UUID of target to be scanned
            scanner_id: UUID of scanner to use for scanning the target
            comment: The comment on the audit.
            alert_ids: List of UUIDs for alerts to be applied to the audit
            hosts_ordering: The order hosts are scanned in
            schedule_id: UUID of a schedule when the audit should be run.
            schedule_periods: A limit to the number of times the audit will be
                scheduled, or 0 for no limit.
            observers: List of names or ids of users which should be allowed to
                observe this audit
            preferences: Name/Value pairs of scanner preferences.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        self.modify_task(
            task_id=audit_id,
            name=name,
            config_id=policy_id,
            target_id=target_id,
            scanner_id=scanner_id,
            alterable=alterable,
            hosts_ordering=hosts_ordering,
            schedule_id=schedule_id,
            schedule_periods=schedule_periods,
            comment=comment,
            alert_ids=alert_ids,
            observers=observers,
            preferences=preferences,
        )

    def modify_policy_set_nvt_preference(
        self,
        policy_id: str,
        name: str,
        nvt_oid: str,
        *,
        value: Optional[str] = None
    ) -> Any:
        """Modifies the nvt preferences of an existing policy.

        Arguments:
            policy_id: UUID of policy to modify.
            name: Name for preference to change.
            nvt_oid: OID of the NVT associated with preference to modify
            value: New value for the preference. None to delete the preference
                and to use the default instead.
        """
        self.modify_config_set_nvt_preference(
            config_id=policy_id,
            name=name,
            nvt_oid=nvt_oid,
            value=value,
        )

    def modify_policy_set_name(self, policy_id: str, name: str) -> Any:
        """Modifies the name of an existing policy

        Arguments:
            config_id: UUID of policy to modify.
            name: New name for the config.
        """
        self.modify_config_set_name(
            config_id=policy_id,
            name=name,
        )

    def modify_policy_set_comment(
        self, policy_id: str, comment: Optional[str] = ""
    ) -> Any:
        """Modifies the comment of an existing policy

        Arguments:
            policy_id: UUID of policy to modify.
            comment: Comment to set on a config. Default: ''
        """
        self.modify_config_set_comment(
            config_id=policy_id,
            comment=comment,
        )

    def modify_policy_set_scanner_preference(
        self, policy_id: str, name: str, *, value: Optional[str] = None
    ) -> Any:
        """Modifies the scanner preferences of an existing policy

        Arguments:
            policy_id: UUID of policy to modify.
            name: Name of the scanner preference to change
            value: New value for the preference. None to delete the preference
                and to use the default instead.

        """
        self.modify_config_set_scanner_preference(
            config_id=policy_id,
            name=name,
            value=value,
        )

    def modify_policy_set_nvt_selection(
        self, policy_id: str, family: str, nvt_oids: List[str]
    ) -> Any:
        """Modifies the selected nvts of an existing policy

        The manager updates the given family in the config to include only the
        given NVTs.

        Arguments:
            policy_id: UUID of policy to modify.
            family: Name of the NVT family to include NVTs from
            nvt_oids: List of NVTs to select for the family.
        """
        self.modify_config_set_nvt_selection(
            config_id=policy_id,
            family=family,
            nvt_oids=nvt_oids,
        )

    def modify_policy_set_family_selection(
        self,
        policy_id: str,
        families: List[str],
        *,
        auto_add_new_families: Optional[bool] = True,
        auto_add_new_nvts: Optional[bool] = True
    ) -> Any:
        """
        Selected the NVTs of a policy at a family level.

        Arguments:
            policy_id: UUID of policy to modify.
            families: List of NVT family names to select.
            auto_add_new_families: Whether new families should be added to the
                policy automatically. Default: True.
            auto_add_new_nvts: Whether new NVTs in the selected families should
                be added to the policy automatically. Default: True.
        """
        self.modify_config_set_family_selection(
            config_id=policy_id,
            families=families,
            auto_add_new_families=auto_add_new_families,
            auto_add_new_nvts=auto_add_new_nvts,
        )

    def modify_tls_certificate(
        self,
        tls_certificate_id: str,
        *,
        name: Optional[str] = None,
        comment: Optional[str] = None,
        trust: Optional[bool] = None
    ) -> Any:
        """Modifies an existing TLS certificate.

        Arguments:
            tls_certificate_id: UUID of the TLS certificate to be modified.
            name: Name of the TLS certificate, defaulting to the MD5 fingerprint
            comment: Comment for the TLS certificate.
            trust: Whether the certificate is trusted.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not tls_certificate_id:
            raise RequiredArgument(
                function=self.modify_tls_certificate.__name__,
                argument='tls_certificate_id',
            )

        cmd = XmlCommand("modify_tls_certificate")
        cmd.set_attribute("tls_certificate_id", str(tls_certificate_id))

        if comment:
            cmd.add_element("comment", comment)

        if name:
            cmd.add_element("name", name)

        if trust:
            cmd.add_element("trust", _to_bool(trust))

        return self._send_xml_command(cmd)

    def clone_tls_certificate(self, tls_certificate_id: str) -> Any:
        """Modifies an existing TLS certificate.

        Arguments:
            tls_certificate_id: The UUID of an existing TLS certificate

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not tls_certificate_id:
            raise RequiredArgument(
                function=self.clone_tls_certificate.__name__,
                argument='tls_certificate_id',
            )

        cmd = XmlCommand("create_tls_certificate")

        cmd.add_element("copy", tls_certificate_id)

        return self._send_xml_command(cmd)

    def get_configs(
        self,
        *,
        filter: Optional[str] = None,
        filter_id: Optional[str] = None,
        trash: Optional[bool] = None,
        details: Optional[bool] = None,
        families: Optional[bool] = None,
        preferences: Optional[bool] = None,
        tasks: Optional[bool] = None
    ) -> Any:
        """Request a list of scan configs

        Arguments:
            filter: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get the trashcan scan configs instead
            details: Whether to get config families, preferences, nvt selectors
                and tasks.
            families: Whether to include the families if no details are
                requested
            preferences: Whether to include the preferences if no details are
                requested
            tasks: Whether to get tasks using this config

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        return self.__get_configs(
            UsageType.SCAN,
            filter=filter,
            filter_id=filter_id,
            trash=trash,
            details=details,
            families=families,
            preferences=preferences,
            tasks=tasks,
        )

    def get_policies(
        self,
        *,
        audits: Optional[bool] = None,
        filter: Optional[str] = None,
        filter_id: Optional[str] = None,
        details: Optional[bool] = None,
        families: Optional[bool] = None,
        preferences: Optional[bool] = None,
        trash: Optional[bool] = None
    ) -> Any:
        """Request a list of policies

        Arguments:
            audits: Whether to get audits using the policy
            filter: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            details: Whether to get  families, preferences, nvt selectors
                and tasks.
            families: Whether to include the families if no details are
                requested
            preferences: Whether to include the preferences if no details are
                requested
            trash: Whether to get the trashcan audits instead

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        return self.__get_configs(
            UsageType.POLICY,
            filter=filter,
            filter_id=filter_id,
            details=details,
            families=families,
            preferences=preferences,
            tasks=audits,
            trash=trash,
        )

    def get_config(
        self, config_id: str, *, tasks: Optional[bool] = None
    ) -> Any:
        """Request a single scan config

        Arguments:
            config_id: UUID of an existing scan config
            tasks: Whether to get tasks using this config

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        return self.__get_config(
            config_id=config_id, usage_type=UsageType.SCAN, tasks=tasks
        )

    def get_policy(self, policy_id: str) -> Any:
        """Request a single policy

        Arguments:
            policy_id: UUID of an existing policy

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        return self.__get_config(policy_id, UsageType.POLICY)

    def get_tasks(
        self,
        *,
        filter: Optional[str] = None,
        filter_id: Optional[str] = None,
        trash: Optional[bool] = None,
        details: Optional[bool] = None,
        schedules_only: Optional[bool] = None
    ) -> Any:
        """Request a list of tasks

        Arguments:
            filter: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get the trashcan tasks instead
            details: Whether to include full task details
            schedules_only: Whether to only include id, name and schedule
                details

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        return self.__get_tasks(
            UsageType.SCAN,
            filter=filter,
            filter_id=filter_id,
            trash=trash,
            details=details,
            schedules_only=schedules_only,
        )

    def get_audits(
        self,
        *,
        filter: Optional[str] = None,
        filter_id: Optional[str] = None,
        trash: Optional[bool] = None,
        details: Optional[bool] = None,
        schedules_only: Optional[bool] = None
    ) -> Any:
        """Request a list of audits

        Arguments:
            filter: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get the trashcan audits instead
            details: Whether to include full audit details
            schedules_only: Whether to only include id, name and schedule
                details

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        return self.__get_tasks(
            UsageType.AUDIT,
            filter=filter,
            filter_id=filter_id,
            trash=trash,
            details=details,
            schedules_only=schedules_only,
        )

    def get_task(self, task_id: str) -> Any:
        """Request a single task

        Arguments:
            task_id: UUID of an existing task

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        return self.__get_task(task_id, UsageType.SCAN)

    def get_audit(self, audit_id: str) -> Any:
        """Request a single audit

        Arguments:
            audit_id: UUID of an existing audit

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        return self.__get_task(audit_id, UsageType.AUDIT)

    def clone_audit(self, audit_id: str) -> Any:
        """Clone an existing audit

        Arguments:
            audit_id: UUID of existing audit to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not audit_id:
            raise RequiredArgument(
                function=self.clone_audit.__name__, argument='audit_id'
            )

        cmd = XmlCommand("create_task")
        cmd.add_element("copy", audit_id)
        return self._send_xml_command(cmd)

    def clone_policy(self, policy_id: str) -> Any:
        """Clone a policy from an existing one

        Arguments:
            policy_id: UUID of the existing policy

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not policy_id:
            raise RequiredArgument(
                function=self.clone_policy.__name__, argument='policy_id'
            )

        cmd = XmlCommand("create_config")
        cmd.add_element("copy", policy_id)
        return self._send_xml_command(cmd)

    def delete_audit(
        self, audit_id: str, *, ultimate: Optional[bool] = False
    ) -> Any:
        """Deletes an existing audit

        Arguments:
            audit_id: UUID of the audit to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not audit_id:
            raise RequiredArgument(
                function=self.delete_audit.__name__, argument='audit_id'
            )

        cmd = XmlCommand("delete_task")
        cmd.set_attribute("task_id", audit_id)
        cmd.set_attribute("ultimate", _to_bool(ultimate))

        return self._send_xml_command(cmd)

    def delete_policy(
        self, policy_id: str, *, ultimate: Optional[bool] = False
    ) -> Any:
        """Deletes an existing policy

        Arguments:
            policy_id: UUID of the policy to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not policy_id:
            raise RequiredArgument(
                function=self.delete_policy.__name__, argument='policy_id'
            )

        cmd = XmlCommand("delete_config")
        cmd.set_attribute("config_id", policy_id)
        cmd.set_attribute("ultimate", _to_bool(ultimate))

        return self._send_xml_command(cmd)

    def delete_tls_certificate(self, tls_certificate_id: str) -> Any:
        """Deletes an existing tls certificate

        Arguments:
            tls_certificate_id: UUID of the tls certificate to be deleted.
        """
        if not tls_certificate_id:
            raise RequiredArgument(
                function=self.delete_tls_certificate.__name__,
                argument='tls_certificate_id',
            )

        cmd = XmlCommand("delete_tls_certificate")
        cmd.set_attribute("tls_certificate_id", tls_certificate_id)

        return self._send_xml_command(cmd)

    def __create_task(
        self,
        name: str,
        config_id: str,
        target_id: str,
        scanner_id: str,
        usage_type: UsageType,
        function: str,
        *,
        alterable: Optional[bool] = None,
        hosts_ordering: Optional[HostsOrdering] = None,
        schedule_id: Optional[str] = None,
        alert_ids: Optional[List[str]] = None,
        comment: Optional[str] = None,
        schedule_periods: Optional[int] = None,
        observers: Optional[List[str]] = None,
        preferences: Optional[dict] = None
    ) -> Any:
        if not name:
            raise RequiredArgument(function=function, argument='name')

        if not config_id:
            raise RequiredArgument(function=function, argument='config_id')

        if not target_id:
            raise RequiredArgument(function=function, argument='target_id')

        if not scanner_id:
            raise RequiredArgument(function=function, argument='scanner_id')

        # don't allow to create a container task with create_task
        if target_id == '0':
            raise InvalidArgument(function=function, argument='target_id')

        cmd = XmlCommand("create_task")
        cmd.add_element("name", name)
        cmd.add_element("usage_type", usage_type.value)
        cmd.add_element("config", attrs={"id": config_id})
        cmd.add_element("target", attrs={"id": target_id})
        cmd.add_element("scanner", attrs={"id": scanner_id})

        if comment:
            cmd.add_element("comment", comment)

        if alterable is not None:
            cmd.add_element("alterable", _to_bool(alterable))

        if hosts_ordering:
            if not isinstance(hosts_ordering, self.types.HostsOrdering):
                raise InvalidArgumentType(
                    function=function,
                    argument='hosts_ordering',
                    arg_type=HostsOrdering.__name__,
                )
            cmd.add_element("hosts_ordering", hosts_ordering.value)

        if alert_ids:
            if isinstance(alert_ids, str):
                deprecation(
                    "Please pass a list as alert_ids parameter to {}. "
                    "Passing a string is deprecated and will be removed in "
                    "future.".format(function)
                )

                # if a single id is given as a string wrap it into a list
                alert_ids = [alert_ids]
            if _is_list_like(alert_ids):
                # parse all given alert id's
                for alert in alert_ids:
                    cmd.add_element("alert", attrs={"id": str(alert)})

        if schedule_id:
            cmd.add_element("schedule", attrs={"id": schedule_id})

            if schedule_periods is not None:
                if (
                    not isinstance(schedule_periods, numbers.Integral)
                    or schedule_periods < 0
                ):
                    raise InvalidArgument(
                        "schedule_periods must be an integer greater or equal "
                        "than 0"
                    )
                cmd.add_element("schedule_periods", str(schedule_periods))

        if observers is not None:
            if not _is_list_like(observers):
                raise InvalidArgumentType(
                    function=function, argument='observers', arg_type='list'
                )

            # gvmd splits by comma and space
            # gvmd tries to lookup each value as user name and afterwards as
            # user id. So both user name and user id are possible
            cmd.add_element("observers", _to_comma_list(observers))

        if preferences is not None:
            if not isinstance(preferences, collections.abc.Mapping):
                raise InvalidArgumentType(
                    function=function,
                    argument='preferences',
                    arg_type=collections.abc.Mapping.__name__,
                )

            _xmlprefs = cmd.add_element("preferences")
            for pref_name, pref_value in preferences.items():
                _xmlpref = _xmlprefs.add_element("preference")
                _xmlpref.add_element("scanner_name", pref_name)
                _xmlpref.add_element("value", str(pref_value))

        return self._send_xml_command(cmd)

    def __create_config(
        self,
        config_id: str,
        name: str,
        usage_type: UsageType,
        function: str,
        *,
        comment: Optional[str] = None
    ) -> Any:
        if not name:
            raise RequiredArgument(function=function, argument='name')

        if not config_id:
            raise RequiredArgument(function=function, argument='config_id')

        cmd = XmlCommand("create_config")
        if comment is not None:
            cmd.add_element("comment", comment)
        cmd.add_element("copy", config_id)
        cmd.add_element("name", name)
        cmd.add_element("usage_type", usage_type.value)
        return self._send_xml_command(cmd)

    def __create_config_from_osp_scanner(
        self,
        scanner_id: str,
        name: str,
        usage_type: UsageType,
        function: str,
        *,
        comment: Optional[str] = None
    ) -> Any:
        if not name:
            raise RequiredArgument(function=function, argument='name')

        if not scanner_id:
            raise RequiredArgument(function=function, argument='scanner_id')

        cmd = XmlCommand("create_config")
        if comment is not None:
            cmd.add_element("comment", comment)
        cmd.add_element("scanner", scanner_id)
        cmd.add_element("name", name)
        cmd.add_element("usage_type", usage_type.value)
        return self._send_xml_command(cmd)

    def __get_configs(
        self,
        usage_type: UsageType,
        *,
        filter: Optional[str] = None,
        filter_id: Optional[str] = None,
        trash: Optional[bool] = None,
        details: Optional[bool] = None,
        families: Optional[bool] = None,
        preferences: Optional[bool] = None,
        tasks: Optional[bool] = None
    ) -> Any:
        cmd = XmlCommand("get_configs")
        cmd.set_attribute("usage_type", usage_type.value)

        _add_filter(cmd, filter, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", _to_bool(trash))

        if details is not None:
            cmd.set_attribute("details", _to_bool(details))

        if families is not None:
            cmd.set_attribute("families", _to_bool(families))

        if preferences is not None:
            cmd.set_attribute("preferences", _to_bool(preferences))

        if tasks is not None:
            cmd.set_attribute("tasks", _to_bool(tasks))

        return self._send_xml_command(cmd)

    def __get_config(
        self,
        config_id: str,
        usage_type: UsageType,
        *,
        tasks: Optional[bool] = None
    ) -> Any:
        if not config_id:
            raise RequiredArgument(
                function=self.get_config.__name__, argument='config_id'
            )

        cmd = XmlCommand("get_configs")
        cmd.set_attribute("config_id", config_id)

        cmd.set_attribute("usage_type", usage_type.value)

        if tasks is not None:
            cmd.set_attribute("tasks", _to_bool(tasks))

        # for single entity always request all details
        cmd.set_attribute("details", "1")

        return self._send_xml_command(cmd)

    def __get_tasks(
        self,
        usage_type: UsageType,
        *,
        filter: Optional[str] = None,
        filter_id: Optional[str] = None,
        trash: Optional[bool] = None,
        details: Optional[bool] = None,
        schedules_only: Optional[bool] = None
    ) -> Any:
        cmd = XmlCommand("get_tasks")
        cmd.set_attribute("usage_type", usage_type.value)

        _add_filter(cmd, filter, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", _to_bool(trash))

        if details is not None:
            cmd.set_attribute("details", _to_bool(details))

        if schedules_only is not None:
            cmd.set_attribute("schedules_only", _to_bool(schedules_only))

        return self._send_xml_command(cmd)

    def __get_task(self, task_id: str, usage_type: UsageType) -> Any:
        if not task_id:
            raise RequiredArgument(
                function=self.get_task.__name__, argument='task_id'
            )

        cmd = XmlCommand("get_tasks")
        cmd.set_attribute("task_id", task_id)
        cmd.set_attribute("usage_type", usage_type.value)

        # for single entity always request all details
        cmd.set_attribute("details", "1")
        return self._send_xml_command(cmd)
