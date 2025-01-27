# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


class GmpGetProtocolVersionTestCase:
    def test_protocol_version(self):
        self.assertEqual(self.gmp.get_protocol_version(), (22, 6))
