# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


class GmpGetVersionTestCase:
    def test_get_version(self):
        self.gmp.get_version()

        self.connection.connect.has_been_called()
        self.connection.read.has_been_called()
        self.connection.send.has_been_called()
        self.connection.send.has_been_called_with(b"<get_version/>")
