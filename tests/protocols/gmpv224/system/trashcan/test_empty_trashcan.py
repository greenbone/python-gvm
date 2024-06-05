# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


class GmpEmptyTrashcanTestMixin:
    def test_empty_trashcan(self):
        self.gmp.empty_trashcan()

        self.connection.send.has_been_called_with(b"<empty_trashcan/>")
