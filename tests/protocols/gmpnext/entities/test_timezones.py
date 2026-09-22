# SPDX-FileCopyrightText: 2026 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


from ...gmpnext import GMPTestCase
from .timezones.test_get_timezones import (
    GmpGetTimezonesTestMixin,
)


class GmpGetTimezonesTestCase(GmpGetTimezonesTestMixin, GMPTestCase):
    pass
