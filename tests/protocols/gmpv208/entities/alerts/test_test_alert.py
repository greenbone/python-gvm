# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import GvmError


class GmpTestAlertTestMixin:
    def test_test_alert(self):
        self.gmp.test_alert("a1")

        self.connection.send.has_been_called_with(
            b'<test_alert alert_id="a1"/>'
        )

    def test_missing_id(self):
        with self.assertRaises(GvmError):
            self.gmp.test_alert(None)

        with self.assertRaises(GvmError):
            self.gmp.test_alert("")
