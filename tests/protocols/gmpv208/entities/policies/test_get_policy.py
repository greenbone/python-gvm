# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import GvmError


class GmpGetPolicyTestMixin:
    def test_get_policy(self):
        self.gmp.get_policy("a1")

        self.connection.send.has_been_called_with(
            b'<get_configs config_id="a1" usage_type="policy" details="1"/>'
        )

    def test_get_policy_with_audits(self):
        self.gmp.get_policy("a1", audits=True)

        self.connection.send.has_been_called_with(
            b'<get_configs config_id="a1" '
            b'usage_type="policy" tasks="1" details="1"/>'
        )

    def test_fail_without_policy_id(self):
        with self.assertRaises(GvmError):
            self.gmp.get_policy(None)

        with self.assertRaises(GvmError):
            self.gmp.get_policy("")
