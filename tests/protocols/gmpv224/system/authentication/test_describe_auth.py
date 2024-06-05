# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


class GmpDescribeAuthTestMixin:
    def test_describe_auth(self):
        self.gmp.describe_auth()

        self.connection.send.has_been_called_with(b"<describe_auth/>")
