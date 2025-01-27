# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.core import Request
from gvm.protocols.gmp.requests.v226 import ResourceNames, ResourceType


class ResourceNamesTestCase(unittest.TestCase):
    def test_get_resource_names(self) -> None:
        request = ResourceNames.get_resource_names(ResourceType.ALERT)

        self.assertIsInstance(request, Request)

        self.assertEqual(bytes(request), b'<get_resource_names type="ALERT"/>')

        request = ResourceNames.get_resource_names(ResourceType.CERT_BUND_ADV)

        self.assertEqual(
            bytes(request), b'<get_resource_names type="CERT_BUND_ADV"/>'
        )

        request = ResourceNames.get_resource_names(ResourceType.CONFIG)

        self.assertEqual(bytes(request), b'<get_resource_names type="CONFIG"/>')

        request = ResourceNames.get_resource_names(
            resource_type=ResourceType.CPE
        )

        self.assertEqual(bytes(request), b'<get_resource_names type="CPE"/>')

        request = ResourceNames.get_resource_names(ResourceType.CREDENTIAL)

        self.assertEqual(
            bytes(request), b'<get_resource_names type="CREDENTIAL"/>'
        )

        request = ResourceNames.get_resource_names(ResourceType.CVE)

        self.assertEqual(bytes(request), b'<get_resource_names type="CVE"/>')

        request = ResourceNames.get_resource_names(ResourceType.DFN_CERT_ADV)

        self.assertEqual(
            bytes(request), b'<get_resource_names type="DFN_CERT_ADV"/>'
        )

        request = ResourceNames.get_resource_names(ResourceType.FILTER)

        self.assertEqual(bytes(request), b'<get_resource_names type="FILTER"/>')

        request = ResourceNames.get_resource_names(ResourceType.GROUP)

        self.assertEqual(bytes(request), b'<get_resource_names type="GROUP"/>')

        request = ResourceNames.get_resource_names(ResourceType.HOST)

        self.assertEqual(bytes(request), b'<get_resource_names type="HOST"/>')

        request = ResourceNames.get_resource_names(ResourceType.NOTE)

        self.assertEqual(bytes(request), b'<get_resource_names type="NOTE"/>')

        request = ResourceNames.get_resource_names(ResourceType.NVT)

        self.assertEqual(bytes(request), b'<get_resource_names type="NVT"/>')

        request = ResourceNames.get_resource_names(ResourceType.OS)

        self.assertEqual(bytes(request), b'<get_resource_names type="OS"/>')

        request = ResourceNames.get_resource_names(ResourceType.OVERRIDE)

        self.assertEqual(
            bytes(request), b'<get_resource_names type="OVERRIDE"/>'
        )

        request = ResourceNames.get_resource_names(ResourceType.PERMISSION)

        self.assertEqual(
            bytes(request), b'<get_resource_names type="PERMISSION"/>'
        )

        request = ResourceNames.get_resource_names(ResourceType.PORT_LIST)

        self.assertEqual(
            bytes(request), b'<get_resource_names type="PORT_LIST"/>'
        )

        request = ResourceNames.get_resource_names(ResourceType.REPORT_FORMAT)

        self.assertEqual(
            bytes(request), b'<get_resource_names type="REPORT_FORMAT"/>'
        )

        request = ResourceNames.get_resource_names(ResourceType.REPORT)

        self.assertEqual(bytes(request), b'<get_resource_names type="REPORT"/>')

        request = ResourceNames.get_resource_names(ResourceType.REPORT_CONFIG)

        self.assertEqual(
            bytes(request), b'<get_resource_names type="REPORT_CONFIG"/>'
        )

        request = ResourceNames.get_resource_names(ResourceType.RESULT)

        self.assertEqual(bytes(request), b'<get_resource_names type="RESULT"/>')

        request = ResourceNames.get_resource_names(ResourceType.ROLE)

        self.assertEqual(bytes(request), b'<get_resource_names type="ROLE"/>')

        request = ResourceNames.get_resource_names(ResourceType.SCANNER)

        self.assertEqual(
            bytes(request), b'<get_resource_names type="SCANNER"/>'
        )

        request = ResourceNames.get_resource_names(ResourceType.SCHEDULE)

        self.assertEqual(
            bytes(request), b'<get_resource_names type="SCHEDULE"/>'
        )

        request = ResourceNames.get_resource_names(ResourceType.TARGET)

        self.assertEqual(bytes(request), b'<get_resource_names type="TARGET"/>')

        request = ResourceNames.get_resource_names(ResourceType.TASK)

        self.assertEqual(bytes(request), b'<get_resource_names type="TASK"/>')

        request = ResourceNames.get_resource_names(ResourceType.TLS_CERTIFICATE)

        self.assertEqual(
            bytes(request), b'<get_resource_names type="TLS_CERTIFICATE"/>'
        )

        request = ResourceNames.get_resource_names(ResourceType.USER)

        self.assertEqual(bytes(request), b'<get_resource_names type="USER"/>')

    def test_get_resource_names_missing_resource_type(self) -> None:
        with self.assertRaises(RequiredArgument):
            ResourceNames.get_resource_names(resource_type=None)  # type: ignore

        with self.assertRaises(RequiredArgument):
            ResourceNames.get_resource_names(resource_type="")

        with self.assertRaises(RequiredArgument):
            ResourceNames.get_resource_names("")

    def test_get_resource_names_invalid_resource_type(self) -> None:
        with self.assertRaises(InvalidArgument):
            ResourceNames.get_resource_names(resource_type="foo")

    def test_get_resource_names_with_filter_string(self) -> None:
        request = ResourceNames.get_resource_names(
            ResourceType.CPE, filter_string="foo=bar"
        )

        self.assertEqual(
            bytes(request), b'<get_resource_names type="CPE" filter="foo=bar"/>'
        )

    def test_get_resource_name(self):
        request = ResourceNames.get_resource_name(
            resource_type=ResourceType.ALERT, resource_id="i1"
        )

        self.assertEqual(
            bytes(request),
            b'<get_resource_names resource_id="i1" type="ALERT"/>',
        )

        request = ResourceNames.get_resource_name(
            resource_type=ResourceType.CERT_BUND_ADV, resource_id="i1"
        )

        self.assertEqual(
            bytes(request),
            b'<get_resource_names resource_id="i1" type="CERT_BUND_ADV"/>',
        )

        request = ResourceNames.get_resource_name(
            resource_type=ResourceType.CONFIG, resource_id="i1"
        )

        self.assertEqual(
            bytes(request),
            b'<get_resource_names resource_id="i1" type="CONFIG"/>',
        )

        request = ResourceNames.get_resource_name(
            resource_type=ResourceType.CPE, resource_id="i1"
        )

        self.assertEqual(
            bytes(request), b'<get_resource_names resource_id="i1" type="CPE"/>'
        )

        request = ResourceNames.get_resource_name(
            resource_type=ResourceType.CREDENTIAL, resource_id="i1"
        )

        self.assertEqual(
            bytes(request),
            b'<get_resource_names resource_id="i1" type="CREDENTIAL"/>',
        )

        request = ResourceNames.get_resource_name(
            resource_type=ResourceType.CVE, resource_id="i1"
        )

        self.assertEqual(
            bytes(request), b'<get_resource_names resource_id="i1" type="CVE"/>'
        )

        request = ResourceNames.get_resource_name(
            resource_type=ResourceType.DFN_CERT_ADV, resource_id="i1"
        )

        self.assertEqual(
            bytes(request),
            b'<get_resource_names resource_id="i1" type="DFN_CERT_ADV"/>',
        )

        request = ResourceNames.get_resource_name(
            resource_type=ResourceType.FILTER, resource_id="i1"
        )

        self.assertEqual(
            bytes(request),
            b'<get_resource_names resource_id="i1" type="FILTER"/>',
        )

        request = ResourceNames.get_resource_name(
            resource_type=ResourceType.GROUP, resource_id="i1"
        )

        self.assertEqual(
            bytes(request),
            b'<get_resource_names resource_id="i1" type="GROUP"/>',
        )

        request = ResourceNames.get_resource_name(
            resource_type=ResourceType.HOST, resource_id="i1"
        )

        self.assertEqual(
            bytes(request),
            b'<get_resource_names resource_id="i1" type="HOST"/>',
        )

        request = ResourceNames.get_resource_name(
            resource_type=ResourceType.NOTE, resource_id="i1"
        )

        self.assertEqual(
            bytes(request),
            b'<get_resource_names resource_id="i1" type="NOTE"/>',
        )

        request = ResourceNames.get_resource_name(
            resource_type=ResourceType.NVT, resource_id="i1"
        )

        self.assertEqual(
            bytes(request), b'<get_resource_names resource_id="i1" type="NVT"/>'
        )

        request = ResourceNames.get_resource_name(
            resource_type=ResourceType.OS, resource_id="i1"
        )

        self.assertEqual(
            bytes(request), b'<get_resource_names resource_id="i1" type="OS"/>'
        )

        request = ResourceNames.get_resource_name(
            resource_type=ResourceType.PERMISSION, resource_id="i1"
        )

        self.assertEqual(
            bytes(request),
            b'<get_resource_names resource_id="i1" type="PERMISSION"/>',
        )

        request = ResourceNames.get_resource_name(
            resource_type=ResourceType.PORT_LIST, resource_id="i1"
        )

        self.assertEqual(
            bytes(request),
            b'<get_resource_names resource_id="i1" type="PORT_LIST"/>',
        )

        request = ResourceNames.get_resource_name(
            resource_type=ResourceType.REPORT_FORMAT, resource_id="i1"
        )

        self.assertEqual(
            bytes(request),
            b'<get_resource_names resource_id="i1" type="REPORT_FORMAT"/>',
        )

        request = ResourceNames.get_resource_name(
            resource_type=ResourceType.REPORT, resource_id="i1"
        )

        self.assertEqual(
            bytes(request),
            b'<get_resource_names resource_id="i1" type="REPORT"/>',
        )

        request = ResourceNames.get_resource_name(
            resource_type=ResourceType.REPORT_CONFIG, resource_id="i1"
        )

        self.assertEqual(
            bytes(request),
            b'<get_resource_names resource_id="i1" type="REPORT_CONFIG"/>',
        )

        request = ResourceNames.get_resource_name(
            resource_type=ResourceType.RESULT, resource_id="i1"
        )
        self.assertEqual(
            bytes(request),
            b'<get_resource_names resource_id="i1" type="RESULT"/>',
        )

        request = ResourceNames.get_resource_name(
            resource_type=ResourceType.ROLE, resource_id="i1"
        )

        self.assertEqual(
            bytes(request),
            b'<get_resource_names resource_id="i1" type="ROLE"/>',
        )

        request = ResourceNames.get_resource_name(
            resource_type=ResourceType.SCANNER, resource_id="i1"
        )

        self.assertEqual(
            bytes(request),
            b'<get_resource_names resource_id="i1" type="SCANNER"/>',
        )

        request = ResourceNames.get_resource_name(
            resource_type=ResourceType.SCHEDULE, resource_id="i1"
        )

        self.assertEqual(
            bytes(request),
            b'<get_resource_names resource_id="i1" type="SCHEDULE"/>',
        )

        request = ResourceNames.get_resource_name(
            resource_type=ResourceType.TARGET, resource_id="i1"
        )

        self.assertEqual(
            bytes(request),
            b'<get_resource_names resource_id="i1" type="TARGET"/>',
        )

        request = ResourceNames.get_resource_name(
            resource_type=ResourceType.TASK, resource_id="i1"
        )

        self.assertEqual(
            bytes(request),
            b'<get_resource_names resource_id="i1" type="TASK"/>',
        )

        request = ResourceNames.get_resource_name(
            resource_type=ResourceType.TLS_CERTIFICATE, resource_id="i1"
        )

        self.assertEqual(
            bytes(request),
            b'<get_resource_names resource_id="i1" type="TLS_CERTIFICATE"/>',
        )

        request = ResourceNames.get_resource_name(
            resource_type=ResourceType.USER, resource_id="i1"
        )

        self.assertEqual(
            bytes(request),
            b'<get_resource_names resource_id="i1" type="USER"/>',
        )

    def test_get_resource_name_missing_resource_type(self):
        with self.assertRaises(RequiredArgument):
            ResourceNames.get_resource_name(
                resource_id="i1", resource_type=None
            )

        with self.assertRaises(RequiredArgument):
            ResourceNames.get_resource_name(resource_id="i1", resource_type="")

        with self.assertRaises(RequiredArgument):
            ResourceNames.get_resource_name("i1", "")

    def test_get_resource_name_invalid_resource_type(self):
        with self.assertRaises(InvalidArgument):
            ResourceNames.get_resource_name(
                resource_id="i1", resource_type="foo"
            )

    def test_get_resource_name_missing_resource_id(self):
        with self.assertRaises(RequiredArgument):
            ResourceNames.get_resource_name(
                resource_id="", resource_type=ResourceType.CPE
            )

        with self.assertRaises(RequiredArgument):
            ResourceNames.get_resource_name("", resource_type=ResourceType.CPE)

        with self.assertRaises(RequiredArgument):
            ResourceNames.get_resource_name(
                resource_id=None, resource_type=ResourceType.CPE
            )
