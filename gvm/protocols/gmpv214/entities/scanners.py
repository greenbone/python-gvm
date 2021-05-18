# -*- coding: utf-8 -*-
# Copyright (C) 2021 Greenbone Networks GmbH
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


from enum import Enum
from typing import Optional

from gvm.errors import InvalidArgument


class ScannerType(Enum):
    """Enum for scanner type"""

    OSP_SCANNER_TYPE = "1"
    OPENVAS_SCANNER_TYPE = "2"
    CVE_SCANNER_TYPE = "3"
    GREENBONE_SENSOR_SCANNER_TYPE = "5"


def get_scanner_type_from_string(
    scanner_type: Optional[str],
) -> Optional[ScannerType]:
    """Convert a scanner type string to an actual ScannerType instance

    Arguments:
        scanner_type: Scanner type string to convert to a ScannerType
    """
    if not scanner_type:
        return None

    scanner_type = scanner_type.lower()

    if (
        scanner_type == ScannerType.OSP_SCANNER_TYPE.value
        or scanner_type == 'osp'
    ):
        return ScannerType.OSP_SCANNER_TYPE

    if (
        scanner_type == ScannerType.OPENVAS_SCANNER_TYPE.value
        or scanner_type == 'openvas'
    ):
        return ScannerType.OPENVAS_SCANNER_TYPE

    if (
        scanner_type == ScannerType.CVE_SCANNER_TYPE.value
        or scanner_type == 'cve'
    ):
        return ScannerType.CVE_SCANNER_TYPE

    if (
        scanner_type == ScannerType.GREENBONE_SENSOR_SCANNER_TYPE.value
        or scanner_type == 'greenbone'
    ):
        return ScannerType.GREENBONE_SENSOR_SCANNER_TYPE

    raise InvalidArgument(
        argument='scanner_type', function=get_scanner_type_from_string.__name__
    )
