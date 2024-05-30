# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpCloneAuditTestMixin:
    def test_clone(self):
        self.gmp.clone_audit("a1")

        self.connection.send.has_been_called_with(
            b"<create_task><copy>a1</copy></create_task>"
        )

    def test_missing_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.clone_audit("")

        with self.assertRaises(RequiredArgument):
            self.gmp.clone_audit(None)
