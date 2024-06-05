# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.gmp.requests.v224 import InfoType


class GmpGetInfoTestMixin:
    def test_get_info(self):
        self.gmp.get_info(info_type=InfoType.CERT_BUND_ADV, info_id="i1")

        self.connection.send.has_been_called_with(
            b'<get_info info_id="i1" type="CERT_BUND_ADV" details="1"/>'
        )

        self.gmp.get_info("i1", InfoType.CPE)

        self.connection.send.has_been_called_with(
            b'<get_info info_id="i1" type="CPE" details="1"/>'
        )

        self.gmp.get_info("i1", InfoType.CVE)

        self.connection.send.has_been_called_with(
            b'<get_info info_id="i1" type="CVE" details="1"/>'
        )

        self.gmp.get_info("i1", InfoType.DFN_CERT_ADV)

        self.connection.send.has_been_called_with(
            b'<get_info info_id="i1" type="DFN_CERT_ADV" details="1"/>'
        )

        self.gmp.get_info("i1", InfoType.OVALDEF)

        self.connection.send.has_been_called_with(
            b'<get_info info_id="i1" type="OVALDEF" details="1"/>'
        )

        self.gmp.get_info("i1", InfoType.NVT)

        self.connection.send.has_been_called_with(
            b'<get_info info_id="i1" type="NVT" details="1"/>'
        )

        with self.assertRaises(AttributeError):
            self.gmp.get_info(
                "i1", InfoType.ALLINFO  # pylint: disable=no-member
            )

    def test_get_info_missing_info_type(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_info(info_id="i1", info_type=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_info(info_id="i1", info_type="")

        with self.assertRaises(RequiredArgument):
            self.gmp.get_info("i1", "")

    def test_get_info_invalid_info_type(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.get_info(info_id="i1", info_type="foo")

    def test_get_info_missing_info_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_info(info_id="", info_type=InfoType.CPE)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_info("", info_type=InfoType.CPE)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_info(info_id=None, info_type=InfoType.CPE)
