# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


class GmpGetFeedsTestMixin:
    def test_get_feeds(self):
        self.gmp.get_feeds()

        self.connection.send.has_been_called_with(b"<get_feeds/>")
