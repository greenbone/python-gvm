# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Greenbone Management Protocol (GMP) version 22.5
"""

from typing import Optional

from .._protocol import T
from ._gmp224 import GMPv224
from .requests.v225 import (
    ResourceNames,
    ResourceType,
)


class GMPv225(GMPv224[T]):
    """
    A class implementing the Greenbone Management Protocol (GMP) version 22.5

    Example:

        .. code-block:: python

            from gvm.protocols.gmp import GMPv225 as GMP

            with GMP(connection) as gmp:
                resp = gmp.get_tasks()
    """

    def __init__(self, *args, **kwargs):
        """
        Create a new GMPv225 instance.

        Args:
            connection: Connection to use to talk with the remote daemon. See
                :mod:`gvm.connections` for possible connection types.
            transform: Optional transform `callable`_ to convert response data.
                After each request the callable gets passed the plain response data
                which can be used to check the data and/or conversion into different
                representations like a xml dom.

                See :mod:`gvm.transforms` for existing transforms.

        .. _callable:
            https://docs.python.org/3/library/functions.html#callable
        """
        super().__init__(*args, **kwargs)

    @staticmethod
    def get_protocol_version() -> tuple[int, int]:
        return (22, 5)

    def get_resource_names(
        self,
        resource_type: ResourceType,
        *,
        filter_string: Optional[str] = None,
    ) -> T:
        """Request a list of resource names and IDs

        Arguments:
            resource_type: Type must be either ALERT, CERT_BUND_ADV,
                CONFIG, CPE, CREDENTIAL, CVE, DFN_CERT_ADV, FILTER,
                GROUP, HOST, NOTE, NVT, OS, OVERRIDE, PERMISSION,
                PORT_LIST, REPORT_FORMAT, REPORT, RESULT, ROLE,
                SCANNER, SCHEDULE, TARGET, TASK, TLS_CERTIFICATE
                or USER
            filter_string: Filter term to use for the query
        """
        return self._send_and_transform_command(
            ResourceNames.get_resource_names(
                resource_type, filter_string=filter_string
            )
        )

    def get_resource_name(
        self, resource_id: str, resource_type: ResourceType
    ) -> T:
        """Request a single resource name

        Arguments:
            resource_id: ID of an existing resource
            resource_type: Type must be either ALERT, CERT_BUND_ADV,
                CONFIG, CPE, CREDENTIAL, CVE, DFN_CERT_ADV, FILTER,
                GROUP, HOST, NOTE, NVT, OS, OVERRIDE, PERMISSION,
                PORT_LIST, REPORT_FORMAT, REPORT, RESULT, ROLE,
                SCANNER, SCHEDULE, TARGET, TASK, TLS_CERTIFICATE
                or USER
        """
        return self._send_and_transform_command(
            ResourceNames.get_resource_name(resource_id, resource_type)
        )
