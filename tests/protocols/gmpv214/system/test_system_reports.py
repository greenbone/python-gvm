# SPDX-FileCopyrightText: 2019-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208.system.system_reports import GmpGetSystemReportsTestMixin
from ...gmpv214 import Gmpv214TestCase


class Gmpv214GetSystemReportsTestCase(
    GmpGetSystemReportsTestMixin, Gmpv214TestCase
):
    pass
