# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224.entities.scanners import (
    GmpCloneScannerTestMixin,
    GmpCreateScannerTestMixin,
    GmpDeleteScannerTestMixin,
    GmpGetScannersTestMixin,
    GmpGetScannerTestMixin,
    GmpModifyScannerTestMixin,
)
from ...gmpv226 import GMPTestCase
from gvm.protocols.gmp.requests.v226 import ScannerType

class GMPDeleteScannerTestCase(GmpDeleteScannerTestMixin, GMPTestCase):
    pass


class GMPGetScannerTestCase(GmpGetScannerTestMixin, GMPTestCase):
    pass


class GMPGetScannersTestCase(GmpGetScannersTestMixin, GMPTestCase):
    pass


class GMPCloneScannerTestCase(GmpCloneScannerTestMixin, GMPTestCase):
    pass


class GMPCreateScannerTestCase(GmpCreateScannerTestMixin, GMPTestCase):
    def test_create_scanner_with_openvasd_type(self):
        self.gmp.create_scanner(
            name="foo",
            host="localhost",
            port=1234,
            scanner_type=ScannerType.OPENVASD_SCANNER_TYPE,
            credential_id="c1",
        )

        self.connection.send.has_been_called_with(
            b"<create_scanner>"
            b"<name>foo</name>"
            b"<host>localhost</host>"
            b"<port>1234</port>"
            b"<type>6</type>"
            b'<credential id="c1"/>'
            b"</create_scanner>"
        )

    def test_create_scanner_with_relay_host(self):
        self.gmp.create_scanner(
            name="foo",
            host="remotehost",
            port=1234,
            scanner_type=ScannerType.OPENVASD_SCANNER_TYPE,
            credential_id="c1",
            relay_host="localhost",
        )

        self.connection.send.has_been_called_with(
            b"<create_scanner>"
            b"<name>foo</name>"
            b"<host>remotehost</host>"
            b"<port>1234</port>"
            b"<type>6</type>"
            b'<credential id="c1"/>'
            b'<relay_host>localhost</relay_host>'
            b"</create_scanner>"
        )

    def test_create_scanner_with_relay_port(self):
        self.gmp.create_scanner(
            name="foo",
            host="remotehost",
            port=1234,
            scanner_type=ScannerType.OPENVASD_SCANNER_TYPE,
            credential_id="c1",
            relay_port=2345,
        )

        self.connection.send.has_been_called_with(
            b"<create_scanner>"
            b"<name>foo</name>"
            b"<host>remotehost</host>"
            b"<port>1234</port>"
            b"<type>6</type>"
            b'<credential id="c1"/>'
            b'<relay_port>2345</relay_port>'
            b"</create_scanner>"
        )
class GMPModifyScannerTestCase(GmpModifyScannerTestMixin, GMPTestCase):
    def test_modify_scanner_with_openvasd_type(self):
        self.gmp.modify_scanner(
            scanner_id="s1",
            scanner_type=ScannerType.OPENVASD_SCANNER_TYPE,
        )

        self.connection.send.has_been_called_with(
            b'<modify_scanner scanner_id="s1">'
            b'<type>6</type>'
            b'</modify_scanner>'
        )

    def test_modify_scanner_with_relay_host(self):
        self.gmp.modify_scanner(
            scanner_id="s1",
            relay_host="localhost",
        )

        self.connection.send.has_been_called_with(
            b'<modify_scanner scanner_id="s1">'
            b'<relay_host>localhost</relay_host>'
            b'</modify_scanner>'
        )
    def test_modify_scanner_with_relay_port(self):
        self.gmp.modify_scanner(
            scanner_id="s1",
            relay_port=2345,
        )

        self.connection.send.has_been_called_with(
            b'<modify_scanner scanner_id="s1">'
            b'<relay_port>2345</relay_port>'
            b'</modify_scanner>'
        )
