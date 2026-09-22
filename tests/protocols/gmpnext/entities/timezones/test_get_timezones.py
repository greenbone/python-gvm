# SPDX-FileCopyrightText: 2026 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later


class GmpGetTimezonesTestMixin:
    def test_get_timezones(self):
        self.gmp.get_timezones()

        self.connection.send.has_been_called_with(b"<get_timezones/>")
