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

# pylint: disable=too-many-lines,redefined-builtin
"""
Module for communication with gvmd in `Greenbone Management Protocol version 9`_

.. _Greenbone Management Protocol version 9:
    https://docs.greenbone.net/API/GMP/gmp-9.0.html
"""

from typing import Any, Callable, Optional

from gvm.protocols.gmpv9.gmpv9 import GmpV9Mixin
from gvm.protocols.gmpv8.gmpv8 import GmpV8Mixin
from gvm.protocols.gmpv7.gmpv7 import GmpV7Mixin
from gvm.connections import GvmConnection


from . import types
from .types import _UsageType as UsageType
from .types import *  # pylint: disable=unused-wildcard-import, wildcard-import

PROTOCOL_VERSION = (9,)


class Gmp(GmpV9Mixin, GmpV8Mixin, GmpV7Mixin):

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

    @staticmethod
    def get_protocol_version() -> tuple:
        """Determine the Greenbone Management Protocol version.

        Returns:
            tuple: Implemented version of the Greenbone Management Protocol
        """
        return PROTOCOL_VERSION
