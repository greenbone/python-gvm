# SPDX-FileCopyrightText: 2019-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208 import Gmpv208TestCase
from .system_reports import GmpGetSystemReportsTestMixin


class Gmpv208GetSystemReportsTestCase(
    GmpGetSystemReportsTestMixin, Gmpv208TestCase
):
    pass
