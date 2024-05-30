# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpClonePortListTestMixin:
    def test_clone(self):
        self.gmp.clone_port_list("a1")

        self.connection.send.has_been_called_with(
            b"<create_port_list><copy>a1</copy></create_port_list>"
        )

    def test_missing_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.clone_port_list("")

        with self.assertRaises(RequiredArgument):
            self.gmp.clone_port_list(None)
