# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from . import Gmpv224TestCase


class GmpWithStatementTestMixin:
    def test_with_statement(self):
        self.connection.connect.has_not_been_called()
        self.connection.disconnect.has_not_been_called()

        with self.gmp:
            pass

        self.connection.connect.has_been_called()
        self.connection.disconnect.has_been_called()


class Gmpv224WithStatementTestCase(GmpWithStatementTestMixin, Gmpv224TestCase):
    pass
