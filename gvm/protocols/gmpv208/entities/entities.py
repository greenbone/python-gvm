# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


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

    @classmethod
    def from_string(
        cls,
        entity_type: Optional[str],
    ) -> Optional["EntityType"]:
        """Convert a entity type string to an actual EntityType instance

        Arguments:
            entity_type: Entity type string to convert to a EntityType
        """
        if not entity_type:
            return None

        if entity_type == "vuln":
            return cls.VULNERABILITY

        if entity_type == "os":
            return cls.OPERATING_SYSTEM

        if entity_type == "config":
            return cls.SCAN_CONFIG

        if entity_type == "tls_certificate":
            return cls.TLS_CERTIFICATE

        try:
            return cls[entity_type.upper()]
        except KeyError:
            raise InvalidArgument(
                argument="entity_type",
                function=cls.from_string.__name__,
            ) from None
