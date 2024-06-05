# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.gmp.requests.v224 import ScannerType


class GmpModifyScannerTestMixin:
    def test_modify_scanner(self):
        self.gmp.modify_scanner(scanner_id="s1")

        self.connection.send.has_been_called_with(
            b'<modify_scanner scanner_id="s1"/>'
        )

    def test_modify_scanner_missing_scanner_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_scanner(scanner_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_scanner(scanner_id="")

    def test_modify_scanner_with_comment(self):
        self.gmp.modify_scanner(scanner_id="s1", comment="foo")

        self.connection.send.has_been_called_with(
            b'<modify_scanner scanner_id="s1">'
            b"<comment>foo</comment>"
            b"</modify_scanner>"
        )

    def test_modify_scanner_with_host(self):
        self.gmp.modify_scanner(scanner_id="s1", host="foo")

        self.connection.send.has_been_called_with(
            b'<modify_scanner scanner_id="s1">'
            b"<host>foo</host>"
            b"</modify_scanner>"
        )

    def test_modify_scanner_with_port(self):
        self.gmp.modify_scanner(scanner_id="s1", port=1234)

        self.connection.send.has_been_called_with(
            b'<modify_scanner scanner_id="s1">'
            b"<port>1234</port>"
            b"</modify_scanner>"
        )

        self.gmp.modify_scanner(scanner_id="s1", port="1234")

        self.connection.send.has_been_called_with(
            b'<modify_scanner scanner_id="s1">'
            b"<port>1234</port>"
            b"</modify_scanner>"
        )

    def test_modify_scanner_with_name(self):
        self.gmp.modify_scanner(scanner_id="s1", name="foo")

        self.connection.send.has_been_called_with(
            b'<modify_scanner scanner_id="s1">'
            b"<name>foo</name>"
            b"</modify_scanner>"
        )

    def test_modify_scanner_with_ca_pub(self):
        self.gmp.modify_scanner(scanner_id="s1", ca_pub="foo")

        self.connection.send.has_been_called_with(
            b'<modify_scanner scanner_id="s1">'
            b"<ca_pub>foo</ca_pub>"
            b"</modify_scanner>"
        )

    def test_modify_scanner_with_credential_id(self):
        self.gmp.modify_scanner(scanner_id="s1", credential_id="c1")

        self.connection.send.has_been_called_with(
            b'<modify_scanner scanner_id="s1">'
            b'<credential id="c1"/>'
            b"</modify_scanner>"
        )

    def test_modify_scanner_with_scanner_type(self):
        self.gmp.modify_scanner(
            scanner_id="s1", scanner_type=ScannerType.OPENVAS_SCANNER_TYPE
        )

        self.connection.send.has_been_called_with(
            b'<modify_scanner scanner_id="s1">'
            b"<type>2</type>"
            b"</modify_scanner>"
        )

        self.gmp.modify_scanner(
            scanner_id="s1", scanner_type=ScannerType.CVE_SCANNER_TYPE
        )

        self.connection.send.has_been_called_with(
            b'<modify_scanner scanner_id="s1">'
            b"<type>3</type>"
            b"</modify_scanner>"
        )

        self.gmp.modify_scanner(
            scanner_id="s1",
            scanner_type=ScannerType.GREENBONE_SENSOR_SCANNER_TYPE,
        )

        self.connection.send.has_been_called_with(
            b'<modify_scanner scanner_id="s1">'
            b"<type>5</type>"
            b"</modify_scanner>"
        )

    def test_modify_scanner_invalid_scanner_type(self):
        with self.assertRaises(ValueError):
            self.gmp.modify_scanner(scanner_id="s1", scanner_type="")

        with self.assertRaises(InvalidArgument):
            self.gmp.modify_scanner(scanner_id="s1", scanner_type="-1")

        with self.assertRaises(InvalidArgument):
            self.gmp.modify_scanner(scanner_id="s1", scanner_type=1)
