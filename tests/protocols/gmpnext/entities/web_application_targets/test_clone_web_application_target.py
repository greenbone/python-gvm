#  SPDX-FileCopyrightText: 2026 Greenbone AG
#
#  SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpCloneWebApplicationTargetTestMixin:
    TARGET_ID = "00000000-0000-0000-0000-000000000000"

    def test_clone(self):
        self.gmp.clone_web_application_target(self.TARGET_ID)

        self.connection.send.has_been_called_with(
            "<create_web_application_target>"
            f"<copy>{self.TARGET_ID}</copy>"
            "</create_web_application_target>".encode()
        )

    def test_missing_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.clone_web_application_target("")

        with self.assertRaises(RequiredArgument):
            self.gmp.clone_web_application_target(None)
