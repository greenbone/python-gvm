# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpGetCertBundTestMixin:
    def test_get_cert_bund_advisory(self):
        self.gmp.get_cert_bund_advisory(cert_id="i1")

        self.connection.send.has_been_called_with(
            b'<get_info info_id="i1" type="CERT_BUND_ADV" details="1"/>'
        )

        self.gmp.get_cert_bund_advisory("i1")

        self.connection.send.has_been_called_with(
            b'<get_info info_id="i1" type="CERT_BUND_ADV" details="1"/>'
        )

    def test_get_cert_bund_advisory_missing_cert_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_cert_bund_advisory(cert_id="")

        with self.assertRaises(RequiredArgument):
            self.gmp.get_cert_bund_advisory("")

        with self.assertRaises(RequiredArgument):
            self.gmp.get_cert_bund_advisory(cert_id=None)
