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


class ReportFormatType(Enum):
    """Enum for builtin report formats"""

    ANONYMOUS_XML = '5057e5cc-b825-11e4-9d0e-28d24461215b'
    ARF = '910200ca-dc05-11e1-954f-406186ea4fc5'
    CPE = '5ceff8ba-1f62-11e1-ab9f-406186ea4fc5'
    CSV_HOSTS = '9087b18c-626c-11e3-8892-406186ea4fc5"'
    CSV_RESULTS = 'c1645568-627a-11e3-a660-406186ea4fc5'
    GCR_PDF = 'dc51a40a-c022-11e9-b02d-3f7ca5bdcb11'
    GSR_HTML = 'ffa123c9-a2d2-409e-bbbb-a6c1385dbeaa'
    GSR_PDF = '35ba7077-dc85-42ef-87c9-b0eda7e903b6'
    GXCR_PDF = 'f0d348de-c022-11e9-bc4c-4bf1d5e1a8ca'
    GXR_PDF = 'ebbc7f34-8ae5-11e1-b07b-001f29eadec8'
    ITG = '77bd6c4a-1f62-11e1-abf0-406186ea4fc5'
    LATEX = 'a684c02c-b531-11e1-bdc2-406186ea4fc5'
    NBE = '9ca6fe72-1f62-11e1-9e7c-406186ea4fc5'
    PDF = 'c402cc3e-b531-11e1-9163-406186ea4fc5'
    SVG = '9e5e5deb-879e-4ecc-8be6-a71cd0875cdd'
    TXT = 'a3810a62-1f62-11e1-9219-406186ea4fc5'
    VERINICE_ISM = 'c15ad349-bd8d-457a-880a-c7056532ee15'
    VERINICE_ITG = '50c9950a-f326-11e4-800c-28d24461215b'
    XML = 'a994b278-1f62-11e1-96ac-406186ea4fc5'


def get_report_format_id_from_string(
    report_format: Optional[str],
) -> Optional[ReportFormatType]:
    """Convert an report format name into a ReportFormatType instance"""
    if not report_format:
        return None

    report_format = report_format.lower()

    try:
        return ReportFormatType[report_format.replace(' ', '_').upper()]
    except KeyError:
        raise InvalidArgument(
            argument='report_format',
            function=get_report_format_id_from_string.__name__,
        ) from None
