# SPDX-FileCopyrightText: 2019-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208.system.system_reports import GmpGetSystemReportsTestMixin
from ...gmpv224 import Gmpv224TestCase


class Gmpv224GetSystemReportsTestCase(
    GmpGetSystemReportsTestMixin, Gmpv224TestCase
):
    pass
