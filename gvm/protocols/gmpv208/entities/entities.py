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

# pylint:  disable=redefined-builtin
# MAYBE we should change filter to filter_string (everywhere)

from enum import Enum
from typing import Optional
from gvm.errors import InvalidArgument


class EntityType(Enum):
    """Enum for entity types"""

    ALERT = "alert"
    ASSET = "asset"
    AUDIT = "audit"
    CERT_BUND_ADV = "cert_bund_adv"
    CPE = "cpe"
    CREDENTIAL = "credential"
    CVE = "cve"
    DFN_CERT_ADV = "dfn_cert_adv"
    FILTER = "filter"
    GROUP = "group"
    HOST = "host"
    INFO = "info"
    NOTE = "note"
    NVT = "nvt"
    OPERATING_SYSTEM = "os"
    OVALDEF = "ovaldef"
    OVERRIDE = "override"
    PERMISSION = "permission"
    POLICY = "policy"
    PORT_LIST = "port_list"
    REPORT = "report"
    REPORT_FORMAT = "report_format"
    RESULT = "result"
    ROLE = "role"
    SCAN_CONFIG = "config"
    SCANNER = "scanner"
    SCHEDULE = "schedule"
    TAG = "tag"
    TARGET = "target"
    TASK = "task"
    TICKET = "ticket"
    TLS_CERTIFICATE = "tls_certificate"
    USER = "user"
    VULNERABILITY = "vuln"


def get_entity_type_from_string(
    entity_type: Optional[str],
) -> Optional[EntityType]:
    """Convert a entity type string to an actual EntityType instance

    Arguments:
        entity_type: Entity type string to convert to a EntityType
    """
    if not entity_type:
        return None

    if entity_type == 'vuln':
        return EntityType.VULNERABILITY

    if entity_type == 'os':
        return EntityType.OPERATING_SYSTEM

    if entity_type == 'config':
        return EntityType.SCAN_CONFIG

    if entity_type == 'tls_certificate':
        return EntityType.TLS_CERTIFICATE

    try:
        return EntityType[entity_type.upper()]
    except KeyError:
        raise InvalidArgument(
            argument='entity_type',
            function=get_entity_type_from_string.__name__,
        ) from None
