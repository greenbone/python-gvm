# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpCloneAlertTestMixin:
    def test_clone(self):
        self.gmp.clone_alert("a1")

        self.connection.send.has_been_called_with(
            b"<create_alert><copy>a1</copy></create_alert>"
        )

    def test_missing_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.clone_alert("")

        with self.assertRaises(RequiredArgument):
            self.gmp.clone_alert(None)
