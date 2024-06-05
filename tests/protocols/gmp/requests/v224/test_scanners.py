# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.gmp.requests.v224 import Scanners, ScannerType


class ScannersTestCase(unittest.TestCase):

    def test_create_scanner(self):
        request = Scanners.create_scanner(
            "foo",
            "localhost",
            1234,
            scanner_type=ScannerType.OPENVAS_SCANNER_TYPE,
            credential_id="c1",
        )

        self.assertEqual(
            bytes(request),
            b"<create_scanner>"
            b"<name>foo</name>"
            b"<host>localhost</host>"
            b"<port>1234</port>"
            b"<type>2</type>"
            b'<credential id="c1"/>'
            b"</create_scanner>",
        )

    def test_create_scanner_missing_name(self):
        with self.assertRaises(RequiredArgument):
            Scanners.create_scanner(
                None,
                "localhost",
                1234,
                scanner_type=ScannerType.OPENVAS_SCANNER_TYPE,
                credential_id="c1",
            )

        with self.assertRaises(RequiredArgument):
            Scanners.create_scanner(
                "",
                "localhost",
                1234,
                scanner_type="2",
                credential_id="c1",
            )

    def test_create_scanner_missing_host(self):
        with self.assertRaises(RequiredArgument):
            Scanners.create_scanner(
                "foo",
                None,
                1234,
                scanner_type=ScannerType.OPENVAS_SCANNER_TYPE,
                credential_id="c1",
            )

        with self.assertRaises(RequiredArgument):
            Scanners.create_scanner(
                "foo",
                "",
                1234,
                scanner_type="2",
                credential_id="c1",
            )

    def test_create_scanner_missing_port(self):
        with self.assertRaises(RequiredArgument):
            Scanners.create_scanner(
                "foo",
                "localhost",
                None,
                scanner_type=ScannerType.OPENVAS_SCANNER_TYPE,
                credential_id="c1",
            )

        with self.assertRaises(RequiredArgument):
            Scanners.create_scanner(
                "foo",
                "localhost",
                "",
                scanner_type="2",
                credential_id="c1",
            )

    def test_create_scanner_missing_scanner_type(self):
        with self.assertRaises(RequiredArgument):
            Scanners.create_scanner(
                "foo",
                "localhost",
                1234,
                scanner_type=None,
                credential_id="c1",
            )

        with self.assertRaises(RequiredArgument):
            Scanners.create_scanner(
                "foo",
                "localhost",
                1234,
                scanner_type="",
                credential_id="c1",
            )

    def test_create_scanner_missing_credential_id(self):
        with self.assertRaises(RequiredArgument):
            Scanners.create_scanner(
                "foo",
                "localhost",
                1234,
                scanner_type=ScannerType.OPENVAS_SCANNER_TYPE,
                credential_id=None,
            )

        with self.assertRaises(RequiredArgument):
            Scanners.create_scanner(
                "foo",
                "localhost",
                1234,
                scanner_type="2",
                credential_id="",
            )

    def test_create_scanner_invalid_scanner_type(self):
        with self.assertRaises(InvalidArgument):
            Scanners.create_scanner(
                "foo",
                "localhost",
                1234,
                scanner_type="invalid",
                credential_id="c1",
            )

    def test_create_scanner_with_ca_pub(self):
        request = Scanners.create_scanner(
            "foo",
            "localhost",
            1234,
            scanner_type=ScannerType.OPENVAS_SCANNER_TYPE,
            credential_id="c1",
            ca_pub="foo",
        )

        self.assertEqual(
            bytes(request),
            b"<create_scanner>"
            b"<name>foo</name>"
            b"<host>localhost</host>"
            b"<port>1234</port>"
            b"<type>2</type>"
            b'<credential id="c1"/>'
            b"<ca_pub>foo</ca_pub>"
            b"</create_scanner>",
        )

    def test_create_scanner_with_comment(self):
        request = Scanners.create_scanner(
            "foo",
            "localhost",
            1234,
            scanner_type=ScannerType.OPENVAS_SCANNER_TYPE,
            credential_id="c1",
            comment="foo",
        )

        self.assertEqual(
            bytes(request),
            b"<create_scanner>"
            b"<name>foo</name>"
            b"<host>localhost</host>"
            b"<port>1234</port>"
            b"<type>2</type>"
            b'<credential id="c1"/>'
            b"<comment>foo</comment>"
            b"</create_scanner>",
        )

    def test_modify_scanner(self):
        request = Scanners.modify_scanner("s1")

        self.assertEqual(
            bytes(request),
            b'<modify_scanner scanner_id="s1"/>',
        )

    def test_modify_scanner_missing_scanner_id(self):
        with self.assertRaises(RequiredArgument):
            Scanners.modify_scanner(None)

        with self.assertRaises(RequiredArgument):
            Scanners.modify_scanner("")

    def test_modify_scanner_with_comment(self):
        request = Scanners.modify_scanner("s1", comment="foo")

        self.assertEqual(
            bytes(request),
            b'<modify_scanner scanner_id="s1">'
            b"<comment>foo</comment>"
            b"</modify_scanner>",
        )

    def test_modify_scanner_with_host(self):
        request = Scanners.modify_scanner("s1", host="foo")

        self.assertEqual(
            bytes(request),
            b'<modify_scanner scanner_id="s1">'
            b"<host>foo</host>"
            b"</modify_scanner>",
        )

    def test_modify_scanner_with_port(self):
        request = Scanners.modify_scanner("s1", port=1234)

        self.assertEqual(
            bytes(request),
            b'<modify_scanner scanner_id="s1">'
            b"<port>1234</port>"
            b"</modify_scanner>",
        )

        request = Scanners.modify_scanner("s1", port="1234")

        self.assertEqual(
            bytes(request),
            b'<modify_scanner scanner_id="s1">'
            b"<port>1234</port>"
            b"</modify_scanner>",
        )

    def test_modify_scanner_with_name(self):
        request = Scanners.modify_scanner("s1", name="foo")

        self.assertEqual(
            bytes(request),
            b'<modify_scanner scanner_id="s1">'
            b"<name>foo</name>"
            b"</modify_scanner>",
        )

    def test_modify_scanner_with_ca_pub(self):
        request = Scanners.modify_scanner("s1", ca_pub="foo")

        self.assertEqual(
            bytes(request),
            b'<modify_scanner scanner_id="s1">'
            b"<ca_pub>foo</ca_pub>"
            b"</modify_scanner>",
        )

    def test_modify_scanner_with_credential_id(self):
        request = Scanners.modify_scanner("s1", credential_id="c1")

        self.assertEqual(
            bytes(request),
            b'<modify_scanner scanner_id="s1">'
            b'<credential id="c1"/>'
            b"</modify_scanner>",
        )

    def test_modify_scanner_with_scanner_type(self):
        request = Scanners.modify_scanner(
            "s1", scanner_type=ScannerType.OPENVAS_SCANNER_TYPE
        )

        self.assertEqual(
            bytes(request),
            b'<modify_scanner scanner_id="s1">'
            b"<type>2</type>"
            b"</modify_scanner>",
        )

        request = Scanners.modify_scanner("s1", scanner_type="2")

        self.assertEqual(
            bytes(request),
            b'<modify_scanner scanner_id="s1">'
            b"<type>2</type>"
            b"</modify_scanner>",
        )

    def test_modify_scanner_invalid_scanner_type(self):
        with self.assertRaises(InvalidArgument):
            Scanners.modify_scanner("s1", scanner_type="invalid")

        with self.assertRaises(ValueError):
            Scanners.modify_scanner("s1", scanner_type="")

        with self.assertRaises(InvalidArgument):
            Scanners.modify_scanner("s1", scanner_type="-1")

        with self.assertRaises(InvalidArgument):
            Scanners.modify_scanner("s1", scanner_type=1)

    def test_get_scanners(self):
        request = Scanners.get_scanners()

        self.assertEqual(bytes(request), b"<get_scanners/>")

    def test_get_scanners_with_filter_string(self):
        request = Scanners.get_scanners(filter_string="foo=bar")

        self.assertEqual(
            bytes(request),
            b'<get_scanners filter="foo=bar"/>',
        )

    def test_get_scanners_with_filter_id(self):
        request = Scanners.get_scanners(filter_id="f1")

        self.assertEqual(
            bytes(request),
            b'<get_scanners filt_id="f1"/>',
        )

    def test_get_scanners_with_trash(self):
        request = Scanners.get_scanners(trash=True)

        self.assertEqual(
            bytes(request),
            b'<get_scanners trash="1"/>',
        )

        request = Scanners.get_scanners(trash=False)

        self.assertEqual(
            bytes(request),
            b'<get_scanners trash="0"/>',
        )

    def test_get_scanners_with_details(self):
        request = Scanners.get_scanners(details=True)

        self.assertEqual(
            bytes(request),
            b'<get_scanners details="1"/>',
        )

        request = Scanners.get_scanners(details=False)

        self.assertEqual(
            bytes(request),
            b'<get_scanners details="0"/>',
        )

    def test_get_scanner(self):
        request = Scanners.get_scanner("s1")

        self.assertEqual(
            bytes(request),
            b'<get_scanners scanner_id="s1" details="1"/>',
        )

    def test_get_scanner_missing_scanner_id(self):
        with self.assertRaises(RequiredArgument):
            Scanners.get_scanner(None)

        with self.assertRaises(RequiredArgument):
            Scanners.get_scanner("")

    def test_verify_scanner(self):
        request = Scanners.verify_scanner("s1")

        self.assertEqual(
            bytes(request),
            b'<verify_scanner scanner_id="s1"/>',
        )

    def test_verify_scanner_missing_scanner_id(self):
        with self.assertRaises(RequiredArgument):
            Scanners.verify_scanner(None)

        with self.assertRaises(RequiredArgument):
            Scanners.verify_scanner("")

    def test_clone_scanner(self):
        request = Scanners.clone_scanner("s1")

        self.assertEqual(
            bytes(request),
            b"<create_scanner><copy>s1</copy></create_scanner>",
        )

    def test_clone_scanner_missing_scanner_id(self):
        with self.assertRaises(RequiredArgument):
            Scanners.clone_scanner(None)

        with self.assertRaises(RequiredArgument):
            Scanners.clone_scanner("")

    def test_delete_scanner(self):
        request = Scanners.delete_scanner("s1")

        self.assertEqual(
            bytes(request),
            b'<delete_scanner scanner_id="s1" ultimate="0"/>',
        )

    def test_delete_scanner_ultimate(self):
        request = Scanners.delete_scanner("s1", ultimate=True)

        self.assertEqual(
            bytes(request),
            b'<delete_scanner scanner_id="s1" ultimate="1"/>',
        )

        request = Scanners.delete_scanner("s1", ultimate=False)

        self.assertEqual(
            bytes(request),
            b'<delete_scanner scanner_id="s1" ultimate="0"/>',
        )

    def test_delete_scanner_missing_scanner_id(self):
        with self.assertRaises(RequiredArgument):
            Scanners.delete_scanner(None)

        with self.assertRaises(RequiredArgument):
            Scanners.delete_scanner("")
