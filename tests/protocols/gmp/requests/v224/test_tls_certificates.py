# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from gvm.errors import RequiredArgument
from gvm.protocols.gmp.requests.v224 import TLSCertificates


class TLSCertificatesTestCase(unittest.TestCase):
    def test_clone_tls_certificate(self):
        request = TLSCertificates.clone_tls_certificate("tls_certificate_id")
        self.assertEqual(
            bytes(request),
            b"<create_tls_certificate>"
            b"<copy>tls_certificate_id</copy>"
            b"</create_tls_certificate>",
        )

    def test_clone_tls_certificate_missing_tls_certificate_id(self):
        with self.assertRaises(RequiredArgument):
            TLSCertificates.clone_tls_certificate(None)

        with self.assertRaises(RequiredArgument):
            TLSCertificates.clone_tls_certificate("")

    def test_create_tls_certificate(self):
        request = TLSCertificates.create_tls_certificate(
            name="name",
            certificate="certificate",
        )
        self.assertEqual(
            bytes(request),
            b"<create_tls_certificate>"
            b"<name>name</name>"
            b"<certificate>certificate</certificate>"
            b"</create_tls_certificate>",
        )

    def test_create_tls_certificate_with_comment(self):
        request = TLSCertificates.create_tls_certificate(
            name="name",
            certificate="certificate",
            comment="comment",
        )
        self.assertEqual(
            bytes(request),
            b"<create_tls_certificate>"
            b"<name>name</name>"
            b"<certificate>certificate</certificate>"
            b"<comment>comment</comment>"
            b"</create_tls_certificate>",
        )

    def test_create_tls_certificate_with_trust(self):
        request = TLSCertificates.create_tls_certificate(
            name="name",
            certificate="certificate",
            trust=True,
        )
        self.assertEqual(
            bytes(request),
            b"<create_tls_certificate>"
            b"<name>name</name>"
            b"<certificate>certificate</certificate>"
            b"<trust>1</trust>"
            b"</create_tls_certificate>",
        )

        request = TLSCertificates.create_tls_certificate(
            name="name",
            certificate="certificate",
            trust=False,
        )
        self.assertEqual(
            bytes(request),
            b"<create_tls_certificate>"
            b"<name>name</name>"
            b"<certificate>certificate</certificate>"
            b"<trust>0</trust>"
            b"</create_tls_certificate>",
        )

    def test_create_tls_certificate_missing_name(self):
        with self.assertRaises(RequiredArgument):
            TLSCertificates.create_tls_certificate(
                name=None,
                certificate="certificate",
            )

        with self.assertRaises(RequiredArgument):
            TLSCertificates.create_tls_certificate(
                name="",
                certificate="certificate",
            )

    def test_create_tls_certificate_missing_certificate(self):
        with self.assertRaises(RequiredArgument):
            TLSCertificates.create_tls_certificate(
                name="name",
                certificate=None,
            )

        with self.assertRaises(RequiredArgument):
            TLSCertificates.create_tls_certificate(
                name="name",
                certificate="",
            )

    def test_delete_tls_certificate(self):
        request = TLSCertificates.delete_tls_certificate("tls_certificate_id")
        self.assertEqual(
            bytes(request),
            b'<delete_tls_certificate tls_certificate_id="tls_certificate_id"/>',
        )

    def test_delete_tls_certificate_missing_tls_certificate_id(self):
        with self.assertRaises(RequiredArgument):
            TLSCertificates.delete_tls_certificate(None)

        with self.assertRaises(RequiredArgument):
            TLSCertificates.delete_tls_certificate("")

    def test_get_tls_certificates(self):
        request = TLSCertificates.get_tls_certificates()
        self.assertEqual(
            bytes(request),
            b"<get_tls_certificates/>",
        )

    def test_get_tls_certificates_with_filter_string(self):
        request = TLSCertificates.get_tls_certificates(
            filter_string="filter_string"
        )
        self.assertEqual(
            bytes(request),
            b'<get_tls_certificates filter="filter_string"/>',
        )

    def test_get_tls_certificates_with_filter_id(self):
        request = TLSCertificates.get_tls_certificates(filter_id="filter_id")
        self.assertEqual(
            bytes(request),
            b'<get_tls_certificates filt_id="filter_id"/>',
        )

    def test_get_tls_certificates_with_details(self):
        request = TLSCertificates.get_tls_certificates(details=True)
        self.assertEqual(
            bytes(request),
            b'<get_tls_certificates details="1"/>',
        )

        request = TLSCertificates.get_tls_certificates(details=False)
        self.assertEqual(
            bytes(request),
            b'<get_tls_certificates details="0"/>',
        )

    def test_get_tls_certificates_with_include_certificate_data(self):
        request = TLSCertificates.get_tls_certificates(
            include_certificate_data=True
        )
        self.assertEqual(
            bytes(request),
            b'<get_tls_certificates include_certificate_data="1"/>',
        )

        request = TLSCertificates.get_tls_certificates(
            include_certificate_data=False
        )
        self.assertEqual(
            bytes(request),
            b'<get_tls_certificates include_certificate_data="0"/>',
        )

    def test_get_tls_certificate(self):
        request = TLSCertificates.get_tls_certificate("tls_certificate_id")
        self.assertEqual(
            bytes(request),
            b'<get_tls_certificates tls_certificate_id="tls_certificate_id" include_certificate_data="1" details="1"/>',
        )

    def test_get_tls_certificate_missing_tls_certificate_id(self):
        with self.assertRaises(RequiredArgument):
            TLSCertificates.get_tls_certificate(None)

        with self.assertRaises(RequiredArgument):
            TLSCertificates.get_tls_certificate("")

    def test_modify_tls_certificate(self):
        request = TLSCertificates.modify_tls_certificate(
            "tls_certificate_id",
        )
        self.assertEqual(
            bytes(request),
            b'<modify_tls_certificate tls_certificate_id="tls_certificate_id"/>',
        )

    def test_modify_tls_certificate_with_name(self):
        request = TLSCertificates.modify_tls_certificate(
            "tls_certificate_id",
            name="name",
        )
        self.assertEqual(
            bytes(request),
            b'<modify_tls_certificate tls_certificate_id="tls_certificate_id">'
            b"<name>name</name>"
            b"</modify_tls_certificate>",
        )

    def test_modify_tls_certificate_with_comment(self):
        request = TLSCertificates.modify_tls_certificate(
            "tls_certificate_id",
            comment="comment",
        )
        self.assertEqual(
            bytes(request),
            b'<modify_tls_certificate tls_certificate_id="tls_certificate_id">'
            b"<comment>comment</comment>"
            b"</modify_tls_certificate>",
        )

    def test_modify_tls_certificate_with_trust(self):
        request = TLSCertificates.modify_tls_certificate(
            "tls_certificate_id",
            trust=True,
        )
        self.assertEqual(
            bytes(request),
            b'<modify_tls_certificate tls_certificate_id="tls_certificate_id">'
            b"<trust>1</trust>"
            b"</modify_tls_certificate>",
        )

        request = TLSCertificates.modify_tls_certificate(
            "tls_certificate_id",
            trust=False,
        )
        self.assertEqual(
            bytes(request),
            b'<modify_tls_certificate tls_certificate_id="tls_certificate_id">'
            b"<trust>0</trust>"
            b"</modify_tls_certificate>",
        )
