# SPDX-FileCopyrightText: 2019-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest
from unittest.mock import MagicMock, patch

from gvm.errors import GvmError
from gvm.protocols.gmp import Gmp
from gvm.protocols.gmp._gmp224 import GMPv224
from gvm.protocols.gmp._gmp225 import GMPv225
from tests.protocols import GmpTestCase


class GmpContextManagerTestCase(GmpTestCase):
    gmp_class = Gmp

    def test_select_gmpv7(self):
        self.connection.read.return_value(
            b'<get_version_response status="200" status_text="OK">'
            b"<version>7.0</version>"
            b"</get_version_response>"
        )

        with self.assertRaises(GvmError):
            with self.gmp:
                pass

    def test_select_gmpv8(self):
        self.connection.read.return_value(
            b'<get_version_response status="200" status_text="OK">'
            b"<version>8.0</version>"
            b"</get_version_response>"
        )

        with self.assertRaises(GvmError):
            with self.gmp:
                pass

    def test_select_gmpv9(self):
        self.connection.read.return_value(
            b'<get_version_response status="200" status_text="OK">'
            b"<version>9.0</version>"
            b"</get_version_response>"
        )

        with self.assertRaises(GvmError):
            with self.gmp:
                pass

    def test_select_gmpv208(self):
        self.connection.read.return_value(
            b'<get_version_response status="200" status_text="OK">'
            b"<version>20.08</version>"
            b"</get_version_response>"
        )
        with self.assertRaises(GvmError):
            with self.gmp:
                pass

    def test_select_gmpv214(self):
        self.connection.read.return_value(
            b'<get_version_response status="200" status_text="OK">'
            b"<version>21.04</version>"
            b"</get_version_response>"
        )

        with self.assertRaises(GvmError):
            with self.gmp:
                pass

    def test_select_gmpv224(self):
        self.connection.read.return_value(
            b'<get_version_response status="200" status_text="OK">'
            b"<version>22.04</version>"
            b"</get_version_response>"
        )

        with self.gmp as gmp:
            self.assertEqual(gmp.get_protocol_version(), (22, 4))
            self.assertIsInstance(gmp, GMPv224)

    def test_select_gmpv225(self):
        self.connection.read.return_value(
            b'<get_version_response status="200" status_text="OK">'
            b"<version>22.05</version>"
            b"</get_version_response>"
        )

        with self.gmp as gmp:
            self.assertEqual(gmp.get_protocol_version(), (22, 5))
            self.assertIsInstance(gmp, GMPv225)

    def test_unknown_protocol(self):
        self.connection.read.return_value(
            b'<get_version_response status="200" status_text="OK">'
            b"<version>1.0</version>"
            b"</get_version_response>"
        )

        with self.assertRaises(GvmError):
            with self.gmp:
                pass

    def test_missing_version_in_response(self):
        self.connection.read.return_value(
            b'<get_version_response status="200" status_text="OK">'
            b"<foo>bar</foo>"
            b"</get_version_response>"
        )

        with self.assertRaises(GvmError):
            with self.gmp:
                pass

    def test_invalid_response(self):
        self.connection.read.return_value(b"<get_foo_response/>")

        with self.assertRaises(GvmError):
            with self.gmp:
                pass

    @patch("gvm.protocols.gmp._gmp.GMPv224", autospec=True)
    def test_connect_disconnect(self, gmp_mock: MagicMock):
        self.connection.read.return_value(
            b'<get_version_response status="200" status_text="OK">'
            b"<version>22.04</version>"
            b"</get_version_response>"
        )

        with self.gmp:
            gmp_mock.assert_called_once()

        mock_instance = gmp_mock.return_value
        mock_instance.connect.assert_called_once()
        mock_instance.disconnect.assert_called_once()


if __name__ == "__main__":
    unittest.main()
