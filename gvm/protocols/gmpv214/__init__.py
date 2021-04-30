# -*- coding: utf-8 -*-
# Copyright (C) 2020-2021 Greenbone Networks GmbH
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

# pylint: disable=too-many-lines,redefined-builtin

"""
Module for communication with gvmd in
`Greenbone Management Protocol version 21.04`_

.. _Greenbone Management Protocol version 21.04:
    https://docs.greenbone.net/API/GMP/gmp-21.04.html
"""

from typing import Any, Callable, Optional

from gvm.protocols.gmpv208.gmpv208 import GmpV208Mixin
from gvm.protocols.gmpv208.entities.reports import ReportsMixin
from gvm.protocols.gmpv208.entities.report_formats import (
    ReportFormatType,
    get_report_format_id_from_string,
)
from gvm.protocols.gmpv208.entities.tasks import TaskMixin
from gvm.protocols.gmpv214.gmpv214 import GmpV214Mixin
from gvm.connections import GvmConnection


from . import types
from .types import *  # pylint: disable=unused-wildcard-import, wildcard-import

PROTOCOL_VERSION = (21, 4)


class Gmp(GmpV214Mixin, GmpV208Mixin, ReportsMixin, TaskMixin):

    types = types

    def __init__(
        self,
        connection: GvmConnection,
        *,
        transform: Optional[Callable[[str], Any]] = None,
    ):
        super().__init__(connection, transform=transform)

        # Is authenticated on gvmd
        self._authenticated = False

    @staticmethod
    def get_protocol_version() -> tuple:
        """Determine the Greenbone Management Protocol version.

        Returns:
            tuple: Implemented version of the Greenbone Management Protocol
        """
        return PROTOCOL_VERSION
