# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


class GmpGetNvtFamiliesTestMixin:
    def test_get_nvt_families(self):
        self.gmp.get_nvt_families()

        self.connection.send.has_been_called_with(b"<get_nvt_families/>")

    def test_get_nvt_families_with_sort_order(self):
        self.gmp.get_nvt_families(sort_order="foo")

        self.connection.send.has_been_called_with(
            b'<get_nvt_families sort_order="foo"/>'
        )
