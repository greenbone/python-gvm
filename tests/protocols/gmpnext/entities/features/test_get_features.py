# SPDX-FileCopyrightText: 2026 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later


class GmpGetFeaturesTestMixin:
    def test_get_features(self):
        self.gmp.get_features()

        self.connection.send.has_been_called_with(b"<get_features/>")
