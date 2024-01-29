# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import InvalidArgumentType, RequiredArgument
from gvm.protocols.gmpv224 import ScannerType


class GmpCreateScannerTestMixin:
    def test_create_scanner(self):
        self.gmp.create_scanner(
            name="foo",
            host="localhost",
            port=1234,
            scanner_type=ScannerType.OPENVAS_SCANNER_TYPE,
            credential_id="c1",
        )

        self.connection.send.has_been_called_with(
            "<create_scanner>"
            "<name>foo</name>"
            "<host>localhost</host>"
            "<port>1234</port>"
            "<type>2</type>"
            '<credential id="c1"/>'
            "</create_scanner>"
        )

    def test_create_scanner_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_scanner(
                name=None,
                host="localhost",
                port=1234,
                scanner_type=ScannerType.OPENVAS_SCANNER_TYPE,
                credential_id="c1",
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_scanner(
                name="",
                host="localhost",
                port=1234,
                scanner_type="2",
                credential_id="c1",
            )

    def test_create_scanner_missing_host(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_scanner(
                name="foo",
                host=None,
                port=1234,
                scanner_type=ScannerType.OPENVAS_SCANNER_TYPE,
                credential_id="c1",
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_scanner(
                name="foo",
                host="",
                port=1234,
                scanner_type=ScannerType.OPENVAS_SCANNER_TYPE,
                credential_id="c1",
            )

    def test_create_scanner_missing_port(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_scanner(
                name="foo",
                host="localhost",
                port=None,
                scanner_type=ScannerType.OPENVAS_SCANNER_TYPE,
                credential_id="c1",
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_scanner(
                name="foo",
                host="localhost",
                port="",
                scanner_type=ScannerType.OPENVAS_SCANNER_TYPE,
                credential_id="c1",
            )

    def test_create_scanner_missing_scanner_type(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_scanner(
                name="foo",
                host="localhost",
                port=1234,
                scanner_type=None,
                credential_id="c1",
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_scanner(
                name="foo",
                host="localhost",
                port=1234,
                scanner_type="",
                credential_id="c1",
            )

    def test_create_scanner_missing_credential_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_scanner(
                name="foo",
                host="localhost",
                port=1234,
                scanner_type=ScannerType.OPENVAS_SCANNER_TYPE,
                credential_id=None,
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_scanner(
                name="foo",
                host="localhost",
                port=1234,
                scanner_type=ScannerType.OPENVAS_SCANNER_TYPE,
                credential_id="",
            )

    def test_create_scanner_invalid_scanner_type(self):
        with self.assertRaises(InvalidArgumentType):
            self.gmp.create_scanner(
                name="foo",
                host="localhost",
                port=1234,
                scanner_type="bar",
                credential_id="c1",
            )

        with self.assertRaises(AttributeError):
            self.gmp.create_scanner(
                name="foo",
                host="localhost",
                port=1234,
                scanner_type=ScannerType.FOO,  # pylint: disable=no-member
                credential_id="c1",
            )

        with self.assertRaises(InvalidArgumentType):
            self.gmp.create_scanner(
                name="foo",
                host="localhost",
                port=1234,
                scanner_type="55",
                credential_id="c1",
            )

    def test_create_scanner_with_ca_pub(self):
        self.gmp.create_scanner(
            name="foo",
            host="localhost",
            port=1234,
            ca_pub="foo",
            scanner_type=ScannerType.OPENVAS_SCANNER_TYPE,
            credential_id="c1",
        )

        self.connection.send.has_been_called_with(
            "<create_scanner>"
            "<name>foo</name>"
            "<host>localhost</host>"
            "<port>1234</port>"
            "<type>2</type>"
            "<ca_pub>foo</ca_pub>"
            '<credential id="c1"/>'
            "</create_scanner>"
        )

    def test_create_scanner_with_comment(self):
        self.gmp.create_scanner(
            name="foo",
            host="localhost",
            port=1234,
            scanner_type=ScannerType.OPENVAS_SCANNER_TYPE,
            credential_id="c1",
            comment="bar",
        )

        self.connection.send.has_been_called_with(
            "<create_scanner>"
            "<name>foo</name>"
            "<host>localhost</host>"
            "<port>1234</port>"
            "<type>2</type>"
            '<credential id="c1"/>'
            "<comment>bar</comment>"
            "</create_scanner>"
        )
