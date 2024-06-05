# SPDX-FileCopyrightText: 2019-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224 import Gmpv224TestCase
from .system_reports import GmpGetSystemReportsTestMixin


class Gmpv224GetSystemReportsTestCase(
    GmpGetSystemReportsTestMixin, Gmpv224TestCase
):
    pass
