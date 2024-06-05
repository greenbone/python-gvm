# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


class GmpGetNvtPreferencesTestMixin:
    def test_get_nvt_preferences(self):
        self.gmp.get_nvt_preferences()

        self.connection.send.has_been_called_with(b"<get_preferences/>")

    def test_get_nvt_preferences_with_nvt_oid(self):
        self.gmp.get_nvt_preferences(nvt_oid="oid")

        self.connection.send.has_been_called_with(
            b'<get_preferences nvt_oid="oid"/>'
        )
