# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.gmp.requests.v225 import ResourceType


class GmpGetResourceNamesListTestMixin:
    def test_get_resource_names(self):
        self.gmp.get_resource_names(ResourceType.ALERT)

        self.connection.send.has_been_called_with(
            b'<get_resource_names type="ALERT"/>'
        )

        self.gmp.get_resource_names(ResourceType.CERT_BUND_ADV)

        self.connection.send.has_been_called_with(
            b'<get_resource_names type="CERT_BUND_ADV"/>'
        )

        self.gmp.get_resource_names(ResourceType.CONFIG)

        self.connection.send.has_been_called_with(
            b'<get_resource_names type="CONFIG"/>'
        )

        self.gmp.get_resource_names(resource_type=ResourceType.CPE)

        self.connection.send.has_been_called_with(
            b'<get_resource_names type="CPE"/>'
        )

        self.gmp.get_resource_names(ResourceType.CREDENTIAL)

        self.connection.send.has_been_called_with(
            b'<get_resource_names type="CREDENTIAL"/>'
        )

        self.gmp.get_resource_names(ResourceType.CVE)

        self.connection.send.has_been_called_with(
            b'<get_resource_names type="CVE"/>'
        )

        self.gmp.get_resource_names(ResourceType.DFN_CERT_ADV)

        self.connection.send.has_been_called_with(
            b'<get_resource_names type="DFN_CERT_ADV"/>'
        )

        self.gmp.get_resource_names(ResourceType.FILTER)

        self.connection.send.has_been_called_with(
            b'<get_resource_names type="FILTER"/>'
        )

        self.gmp.get_resource_names(ResourceType.GROUP)

        self.connection.send.has_been_called_with(
            b'<get_resource_names type="GROUP"/>'
        )

        self.gmp.get_resource_names(ResourceType.HOST)

        self.connection.send.has_been_called_with(
            b'<get_resource_names type="HOST"/>'
        )

        self.gmp.get_resource_names(ResourceType.NOTE)

        self.connection.send.has_been_called_with(
            b'<get_resource_names type="NOTE"/>'
        )

        self.gmp.get_resource_names(ResourceType.NVT)

        self.connection.send.has_been_called_with(
            b'<get_resource_names type="NVT"/>'
        )

        self.gmp.get_resource_names(ResourceType.OS)

        self.connection.send.has_been_called_with(
            b'<get_resource_names type="OS"/>'
        )

        self.gmp.get_resource_names(ResourceType.OVERRIDE)

        self.connection.send.has_been_called_with(
            b'<get_resource_names type="OVERRIDE"/>'
        )

        self.gmp.get_resource_names(ResourceType.PERMISSION)

        self.connection.send.has_been_called_with(
            b'<get_resource_names type="PERMISSION"/>'
        )

        self.gmp.get_resource_names(ResourceType.PORT_LIST)

        self.connection.send.has_been_called_with(
            b'<get_resource_names type="PORT_LIST"/>'
        )

        self.gmp.get_resource_names(ResourceType.REPORT_FORMAT)

        self.connection.send.has_been_called_with(
            b'<get_resource_names type="REPORT_FORMAT"/>'
        )

        self.gmp.get_resource_names(ResourceType.REPORT)

        self.connection.send.has_been_called_with(
            b'<get_resource_names type="REPORT"/>'
        )

        self.gmp.get_resource_names(ResourceType.RESULT)

        self.connection.send.has_been_called_with(
            b'<get_resource_names type="RESULT"/>'
        )

        self.gmp.get_resource_names(ResourceType.ROLE)

        self.connection.send.has_been_called_with(
            b'<get_resource_names type="ROLE"/>'
        )

        self.gmp.get_resource_names(ResourceType.SCANNER)

        self.connection.send.has_been_called_with(
            b'<get_resource_names type="SCANNER"/>'
        )

        self.gmp.get_resource_names(ResourceType.SCHEDULE)

        self.connection.send.has_been_called_with(
            b'<get_resource_names type="SCHEDULE"/>'
        )

        self.gmp.get_resource_names(ResourceType.TARGET)

        self.connection.send.has_been_called_with(
            b'<get_resource_names type="TARGET"/>'
        )

        self.gmp.get_resource_names(ResourceType.TASK)

        self.connection.send.has_been_called_with(
            b'<get_resource_names type="TASK"/>'
        )

        self.gmp.get_resource_names(ResourceType.TLS_CERTIFICATE)

        self.connection.send.has_been_called_with(
            b'<get_resource_names type="TLS_CERTIFICATE"/>'
        )

        self.gmp.get_resource_names(ResourceType.USER)

        self.connection.send.has_been_called_with(
            b'<get_resource_names type="USER"/>'
        )

        with self.assertRaises(AttributeError):
            self.gmp.get_resource_names(
                ResourceType.ALLRESOURCES  # pylint: disable=no-member
            )

    def test_get_resource_names_missing_resource_type(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_resource_names(resource_type=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_resource_names(resource_type="")

        with self.assertRaises(RequiredArgument):
            self.gmp.get_resource_names("")

    def test_get_resource_names_invalid_resource_type(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.get_resource_names(resource_type="foo")

    def test_get_resource_names_with_filter_string(self):
        self.gmp.get_resource_names(ResourceType.CPE, filter_string="foo=bar")

        self.connection.send.has_been_called_with(
            b'<get_resource_names type="CPE" filter="foo=bar"/>'
        )
