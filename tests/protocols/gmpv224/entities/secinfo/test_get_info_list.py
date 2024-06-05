# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import InvalidArgument, RequiredArgument
from gvm.protocols.gmp.requests.v224 import InfoType


class GmpGetInfoListTestMixin:
    def test_get_info_list(self):
        self.gmp.get_info_list(InfoType.CERT_BUND_ADV)

        self.connection.send.has_been_called_with(
            b'<get_info type="CERT_BUND_ADV"/>'
        )

        self.gmp.get_info_list(InfoType.CPE)

        self.connection.send.has_been_called_with(b'<get_info type="CPE"/>')

        self.gmp.get_info_list(info_type=InfoType.CPE)

        self.connection.send.has_been_called_with(b'<get_info type="CPE"/>')

        self.gmp.get_info_list(InfoType.CVE)

        self.connection.send.has_been_called_with(b'<get_info type="CVE"/>')

        self.gmp.get_info_list(InfoType.DFN_CERT_ADV)

        self.connection.send.has_been_called_with(
            b'<get_info type="DFN_CERT_ADV"/>'
        )

        self.gmp.get_info_list(InfoType.OVALDEF)

        self.connection.send.has_been_called_with(b'<get_info type="OVALDEF"/>')

        self.gmp.get_info_list(InfoType.NVT)

        self.connection.send.has_been_called_with(b'<get_info type="NVT"/>')

        with self.assertRaises(AttributeError):
            self.gmp.get_info_list(
                InfoType.ALLINFO  # pylint: disable=no-member
            )

    def test_get_info_list_missing_info_type(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_info_list(info_type=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_info_list(info_type="")

        with self.assertRaises(RequiredArgument):
            self.gmp.get_info_list("")

    def test_get_info_list_invalid_info_type(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.get_info_list(info_type="foo")

    def test_get_info_list_with_filter_string(self):
        self.gmp.get_info_list(InfoType.CPE, filter_string="foo=bar")

        self.connection.send.has_been_called_with(
            b'<get_info type="CPE" filter="foo=bar"/>'
        )

    def test_get_info_list_with_filter_id(self):
        self.gmp.get_info_list(info_type=InfoType.CPE, filter_id="f1")

        self.connection.send.has_been_called_with(
            b'<get_info type="CPE" filt_id="f1"/>'
        )

    def test_get_info_list_with_name(self):
        self.gmp.get_info_list(info_type=InfoType.CPE, name="foo")

        self.connection.send.has_been_called_with(
            b'<get_info type="CPE" name="foo"/>'
        )

    def test_get_info_list_with_details(self):
        self.gmp.get_info_list(info_type=InfoType.CPE, details=True)

        self.connection.send.has_been_called_with(
            b'<get_info type="CPE" details="1"/>'
        )

        self.gmp.get_info_list(info_type=InfoType.CPE, details=False)

        self.connection.send.has_been_called_with(
            b'<get_info type="CPE" details="0"/>'
        )
