# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpGetDfnCertTestMixin:
    def test_get_cert_bund_advisory(self):
        self.gmp.get_dfn_cert_advisory(cert_id="i1")

        self.connection.send.has_been_called_with(
            b'<get_info info_id="i1" type="DFN_CERT_ADV" details="1"/>'
        )

        self.gmp.get_dfn_cert_advisory("i1")

        self.connection.send.has_been_called_with(
            b'<get_info info_id="i1" type="DFN_CERT_ADV" details="1"/>'
        )

    def test_get_cert_bund_advisory_missing_cert_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_dfn_cert_advisory(cert_id="")

        with self.assertRaises(RequiredArgument):
            self.gmp.get_dfn_cert_advisory("")

        with self.assertRaises(RequiredArgument):
            self.gmp.get_dfn_cert_advisory(cert_id=None)
