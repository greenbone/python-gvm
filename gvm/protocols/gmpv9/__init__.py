# -*- coding: utf-8 -*-
# Copyright (C) 2018 - 2019 Greenbone Networks GmbH
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

from enum import Enum
from typing import Any, List, Optional

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.utils import deprecation
from gvm.xml import XmlCommand

from gvm.protocols.gmpv8 import Gmp as Gmpv8, _to_bool, _add_filter
from gvm.protocols.gmpv7 import _is_list_like, _to_comma_list

from . import types
from .types import *

PROTOCOL_VERSION = (9,)


class Gmp(Gmpv8):

    types = types

    @staticmethod
    def get_protocol_version() -> tuple:
        """Determine the Greenbone Management Protocol version.

        Returns:
            tuple: Implemented version of the Greenbone Management Protocol
        """
        return PROTOCOL_VERSION

    def create_audit(
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
        """Create a new audit task

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

        self.__create_task(
            name=name,
            config_id=config_id,
            target_id=target_id,
            scanner_id=scanner_id,
            usage_type=types._UsageType.AUDIT, # pylint: disable=W0212
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

    def create_config(self, config_id: str, name: str) -> Any:
        """Create a new scan config

        """
        self.__create_config(
            config_id=config_id,
            name=name,
            usage_type=types._UsageType.SCAN, # pylint: disable=W0212
            function=self.create_config.__name__,
        )

    def create_policy(self, config_id: str, name: str) -> Any:
        """Create a new policy config

        """
        self.__create_config(
            config_id=config_id,
            name=name,
            usage_type=types._UsageType.POLICY, # pylint: disable=W0212
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
        self.__create_task(
            name=name,
            config_id=config_id,
            target_id=target_id,
            scanner_id=scanner_id,
            usage_type=types._UsageType.SCAN, # pylint: disable=W0212
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
        copy: Optional[str] = None,
        trust: Optional[bool] = None
    ) -> Any:
        """Create a new TLS certificate

        Arguments:
            comment: Comment for the TLS certificate.
            name: Name of the TLS certificate, defaulting to the MD5 fingerprint
            copy: The UUID of an existing TLS certificate
            trust: Whether the certificate is trusted.
            certificate: The Base64 encoded certificate data (x.509 DER or PEM).
           
        Returns:
            The response. See :py:meth:`send_command`for details.
        """
        if not name:
            raise RequiredArgument(
                argument='name', function=self.create_tls_certificate.__name__
            )
        if not certificate:
            raise RequiredArgument(
                argument="certificate",
                function=self.create_tls_certificate.__name__,
            )

        cmd = XmlCommand("create_tls_certificate")

        if comment:
            cmd.add_element("comment", comment)

        if copy:
            cmd.add_element("copy", copy)

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
        include_certificate_data: Optional[bool] = None
    ) -> Any:
        """Request a list of TLS certificates

        Arguments:
            filter: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query

        Returns:
            The response. See :py:meth:`send_command` for details.
        """

        cmd = XmlCommand("get_tls_certificates")

        _add_filter(cmd, filter, filter_id)

        if include_certificate_data is not None:
            cmd.set_attribute(
                "include_certificate_data", _to_bool(include_certificate_data)
            )

        return self._send_xml_command(cmd)

    def modify_tls_certificate(
        self,
        tls_certificate_id: str,
        *,
        name: Optional[str] = None,
        comment: Optional[str] = None,
        copy: Optional[str] = None,
        trust: Optional[bool] = None
    ) -> Any:
        """Modifies an existing TLS certificate.

        Arguments:
            tls_certificate_id: UUID of the TLS certificate to be modified.
            name: Name of the TLS certificate, defaulting to the MD5 fingerprint
            comment: Comment for the TLS certificate.
            trust: Whether the certificate is trusted.
            copy: The UUID of an existing TLS certificate

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not tls_certificate_id:
            raise RequiredArgument(
                argument="tls_certificate_id",
                function=self.modify_tls_certificate.__name__,
            )

        cmd = XmlCommand("modify_tls_certificate")
        cmd.set_attribute("tls_certificate_id", str(tls_certificate_id))

        if comment:
            cmd.add_element("comment", comment)

        if copy:
            cmd.add_element("copy", copy)

        if name:
            cmd.add_element("name", name)

        if trust:
            cmd.add_element("trust", _to_bool(trust))

        return self._send_xml_command(cmd)

    def __create_task(
        self,
        name: str,
        config_id: str,
        target_id: str,
        scanner_id: str,
        usage_type: types._UsageType, # pylint: disable=W0212
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
            raise RequiredArgument(
                "{} requires a name argument".format(function)
            )

        if not config_id:
            raise RequiredArgument(
                "{} requires a config_id argument".format(function)
            )

        if not target_id:
            raise RequiredArgument(
                "{} requires a target_id argument".format(function)
            )

        if not scanner_id:
            raise RequiredArgument(
                "{} requires a scanner_id argument".format(function)
            )

        # don't allow to create a container task with create_task
        if target_id == '0':
            raise InvalidArgument(
                'Invalid argument {} for target_id'.format(target_id)
            )

        cmd = XmlCommand("create_task")
        cmd.add_element("name", name)
        cmd.add_element("usage_type", usage_type.value)
        cmd.add_element("config", attrs={"id": config_id})
        cmd.add_element("target", attrs={"id": target_id})
        cmd.add_element("scanner", attrs={"id": scanner_id})

        if comment:
            cmd.add_element("comment", comment)

        if not alterable is None:
            cmd.add_element("alterable", _to_bool(alterable))

        if hosts_ordering:
            if not isinstance(hosts_ordering, HostsOrdering):
                raise InvalidArgument(
                    function="create_task", argument="hosts_ordering"
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
                raise InvalidArgument("obeservers argument must be a list")

            # gvmd splits by comma and space
            # gvmd tries to lookup each value as user name and afterwards as
            # user id. So both user name and user id are possible
            cmd.add_element("observers", _to_comma_list(observers))

        if preferences is not None:
            if not isinstance(preferences, collections.abc.Mapping):
                raise InvalidArgument('preferences argument must be a dict')

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
        usage_type: types._UsageType, # pylint: disable=W0212
        function: str,
    ) -> Any:
        if not name:
            raise RequiredArgument("{} requires name argument".format(function))

        if not config_id:
            raise RequiredArgument(
                "{} requires config_id argument".format(function)
            )

        cmd = XmlCommand("create_config")
        cmd.add_element("copy", config_id)
        cmd.add_element("name", name)
        cmd.add_element("usage_type", usage_type.value)
        return self._send_xml_command(cmd)
