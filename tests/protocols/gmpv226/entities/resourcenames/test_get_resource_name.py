# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.gmp.requests.v226 import ResourceType


class GmpGetResourceNameTestMixin:
    def test_get_resource_name(self):
        self.gmp.get_resource_name(
            resource_type=ResourceType.ALERT, resource_id="i1"
        )

        self.connection.send.has_been_called_with(
            b'<get_resource_names resource_id="i1" type="ALERT"/>'
        )

        self.gmp.get_resource_name(
            resource_type=ResourceType.CERT_BUND_ADV, resource_id="i1"
        )

        self.connection.send.has_been_called_with(
            b'<get_resource_names resource_id="i1" type="CERT_BUND_ADV"/>'
        )

        self.gmp.get_resource_name(
            resource_type=ResourceType.CONFIG, resource_id="i1"
        )

        self.connection.send.has_been_called_with(
            b'<get_resource_names resource_id="i1" type="CONFIG"/>'
        )

        self.gmp.get_resource_name(
            resource_type=ResourceType.CPE, resource_id="i1"
        )

        self.connection.send.has_been_called_with(
            b'<get_resource_names resource_id="i1" type="CPE"/>'
        )

        self.gmp.get_resource_name(
            resource_type=ResourceType.CREDENTIAL, resource_id="i1"
        )

        self.connection.send.has_been_called_with(
            b'<get_resource_names resource_id="i1" type="CREDENTIAL"/>'
        )

        self.gmp.get_resource_name(
            resource_type=ResourceType.CVE, resource_id="i1"
        )

        self.connection.send.has_been_called_with(
            b'<get_resource_names resource_id="i1" type="CVE"/>'
        )

        self.gmp.get_resource_name(
            resource_type=ResourceType.DFN_CERT_ADV, resource_id="i1"
        )

        self.connection.send.has_been_called_with(
            b'<get_resource_names resource_id="i1" type="DFN_CERT_ADV"/>'
        )

        self.gmp.get_resource_name(
            resource_type=ResourceType.FILTER, resource_id="i1"
        )

        self.connection.send.has_been_called_with(
            b'<get_resource_names resource_id="i1" type="FILTER"/>'
        )

        self.gmp.get_resource_name(
            resource_type=ResourceType.GROUP, resource_id="i1"
        )

        self.connection.send.has_been_called_with(
            b'<get_resource_names resource_id="i1" type="GROUP"/>'
        )

        self.gmp.get_resource_name(
            resource_type=ResourceType.HOST, resource_id="i1"
        )

        self.connection.send.has_been_called_with(
            b'<get_resource_names resource_id="i1" type="HOST"/>'
        )

        self.gmp.get_resource_name(
            resource_type=ResourceType.NOTE, resource_id="i1"
        )

        self.connection.send.has_been_called_with(
            b'<get_resource_names resource_id="i1" type="NOTE"/>'
        )

        self.gmp.get_resource_name(
            resource_type=ResourceType.NVT, resource_id="i1"
        )

        self.connection.send.has_been_called_with(
            b'<get_resource_names resource_id="i1" type="NVT"/>'
        )

        self.gmp.get_resource_name(
            resource_type=ResourceType.OS, resource_id="i1"
        )

        self.connection.send.has_been_called_with(
            b'<get_resource_names resource_id="i1" type="OS"/>'
        )

        self.gmp.get_resource_name(
            resource_type=ResourceType.PERMISSION, resource_id="i1"
        )

        self.connection.send.has_been_called_with(
            b'<get_resource_names resource_id="i1" type="PERMISSION"/>'
        )

        self.gmp.get_resource_name(
            resource_type=ResourceType.PORT_LIST, resource_id="i1"
        )

        self.connection.send.has_been_called_with(
            b'<get_resource_names resource_id="i1" type="PORT_LIST"/>'
        )

        self.gmp.get_resource_name(
            resource_type=ResourceType.REPORT_FORMAT, resource_id="i1"
        )

        self.connection.send.has_been_called_with(
            b'<get_resource_names resource_id="i1" type="REPORT_FORMAT"/>'
        )

        self.gmp.get_resource_name(
            resource_type=ResourceType.REPORT, resource_id="i1"
        )

        self.connection.send.has_been_called_with(
            b'<get_resource_names resource_id="i1" type="REPORT"/>'
        )

        self.gmp.get_resource_name(
            resource_type=ResourceType.REPORT_CONFIG, resource_id="i1"
        )

        self.connection.send.has_been_called_with(
            b'<get_resource_names resource_id="i1" type="REPORT_CONFIG"/>'
        )

        self.gmp.get_resource_name(
            resource_type=ResourceType.RESULT, resource_id="i1"
        )

        self.connection.send.has_been_called_with(
            b'<get_resource_names resource_id="i1" type="RESULT"/>'
        )

        self.gmp.get_resource_name(
            resource_type=ResourceType.ROLE, resource_id="i1"
        )

        self.connection.send.has_been_called_with(
            b'<get_resource_names resource_id="i1" type="ROLE"/>'
        )

        self.gmp.get_resource_name(
            resource_type=ResourceType.SCANNER, resource_id="i1"
        )

        self.connection.send.has_been_called_with(
            b'<get_resource_names resource_id="i1" type="SCANNER"/>'
        )

        self.gmp.get_resource_name(
            resource_type=ResourceType.SCHEDULE, resource_id="i1"
        )

        self.connection.send.has_been_called_with(
            b'<get_resource_names resource_id="i1" type="SCHEDULE"/>'
        )

        self.gmp.get_resource_name(
            resource_type=ResourceType.TARGET, resource_id="i1"
        )

        self.connection.send.has_been_called_with(
            b'<get_resource_names resource_id="i1" type="TARGET"/>'
        )

        self.gmp.get_resource_name(
            resource_type=ResourceType.TASK, resource_id="i1"
        )

        self.connection.send.has_been_called_with(
            b'<get_resource_names resource_id="i1" type="TASK"/>'
        )

        self.gmp.get_resource_name(
            resource_type=ResourceType.TLS_CERTIFICATE, resource_id="i1"
        )

        self.connection.send.has_been_called_with(
            b'<get_resource_names resource_id="i1" type="TLS_CERTIFICATE"/>'
        )

        self.gmp.get_resource_name(
            resource_type=ResourceType.USER, resource_id="i1"
        )

        self.connection.send.has_been_called_with(
            b'<get_resource_names resource_id="i1" type="USER"/>'
        )

    def test_get_resource_name_missing_resource_type(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_resource_name(resource_id="i1", resource_type=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_resource_name(resource_id="i1", resource_type="")

        with self.assertRaises(RequiredArgument):
            self.gmp.get_resource_name("i1", "")

    def test_get_resource_name_invalid_resource_type(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.get_resource_name(resource_id="i1", resource_type="foo")

    def test_get_resource_name_missing_resource_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_resource_name(
                resource_id="", resource_type=ResourceType.CPE
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.get_resource_name("", resource_type=ResourceType.CPE)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_resource_name(
                resource_id=None, resource_type=ResourceType.CPE
            )
