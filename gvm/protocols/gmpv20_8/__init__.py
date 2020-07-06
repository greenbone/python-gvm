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

.. _Greenbone Management Protocol version 20.08:
    https://docs.greenbone.net/API/GMP/gmp-20.08.html
"""
import collections
import numbers

from typing import Any, List, Optional, Callable

from gvm.utils import deprecation
from gvm.xml import XmlCommand

from gvm.protocols.gmpv7 import (
    _to_bool,
    _add_filter,
    _is_list_like,
    _to_comma_list,
)
from gvm.connections import GvmConnection
from gvm.errors import InvalidArgument, InvalidArgumentType, RequiredArgument

from gvm.protocols.base import GvmProtocol

from . import types
from .types import *

_EMPTY_POLICY_ID = '085569ce-73ed-11df-83c3-002264764cea'

PROTOCOL_VERSION = (20, 8)


class GmpV208Mixin(GvmProtocol):

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

    def create_agent(
        self,
        installer: str,
        signature: str,
        name: str,
        *,
        comment: Optional[str] = None,
        howto_install: Optional[str] = None,
        howto_use: Optional[str] = None
    ) -> Any:
        # pylint: disable=unused-argument
        deprecation(
            "{} is deprecated in version {}{}".format(
                self.create_agent.__name__,
                self.get_protocol_version()[0],
                self.get_protocol_version()[1],
            )
        )

    def clone_agent(self, agent_id: str) -> Any:
        # pylint: disable=unused-argument
        deprecation(
            "{} is deprecated in version {}{}".format(
                self.clone_agent.__name__,
                self.get_protocol_version()[0],
                self.get_protocol_version()[1],
            )
        )

    def modify_agent(
        self,
        agent_id: str,
        *,
        name: Optional[str] = None,
        comment: Optional[str] = None
    ) -> Any:
        # pylint: disable=unused-argument
        deprecation(
            "{} is deprecated in version {}{}".format(
                self.clone_agent.__name__,
                self.get_protocol_version()[0],
                self.get_protocol_version()[1],
            )
        )

    def delete_agent(
        self,
        agent_id: str,
        *,
        ultimate: Optional[bool] = False
        # pylint: disable=unused-argument
    ) -> Any:
        deprecation(
            "{} is deprecated in version {}{}".format(
                self.delete_agent.__name__,
                self.get_protocol_version()[0],
                self.get_protocol_version()[1],
            )
        )

    def verify_agent(self, agent_id: str) -> Any:
        # pylint: disable=unused-argument
        deprecation(
            "{} is deprecated in version {}{}".format(
                self.verify_agent.__name__,
                self.get_protocol_version()[0],
                self.get_protocol_version()[1],
            )
        )

    def get_agent(self, agent_id: str) -> Any:
        # pylint: disable=unused-argument
        deprecation(
            "{} is deprecated in version {}{}".format(
                self.get_agent.__name__,
                self.get_protocol_version()[0],
                self.get_protocol_version()[1],
            )
        )

    def get_info(self, info_id: str, info_type: InfoType) -> Any:
        """Request a single secinfo

        Arguments:
            info_id: UUID of an existing secinfo
            info_type: Type must be either CERT_BUND_ADV, CPE, CVE,
                DFN_CERT_ADV, OVALDEF, NVT or ALLINFO

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not info_type:
            raise RequiredArgument(
                function=self.get_info.__name__, argument='info_type'
            )

        if not isinstance(info_type, InfoType):
            raise InvalidArgumentType(
                function=self.get_info.__name__,
                argument='info_type',
                arg_type=InfoType.__name__,
            )

        if not info_id:
            raise RequiredArgument(
                function=self.get_info.__name__, argument='info_id'
            )

        cmd = XmlCommand("get_info")
        cmd.set_attribute("info_id", info_id)

        cmd.set_attribute("type", info_type.value)

        # for single entity always request all details
        cmd.set_attribute("details", "1")
        return self._send_xml_command(cmd)
