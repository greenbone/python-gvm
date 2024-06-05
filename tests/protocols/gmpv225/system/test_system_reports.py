# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224.system.system_reports import GmpGetSystemReportsTestMixin
from ...gmpv225 import Gmpv225TestCase


class Gmpv225GetSystemReportsTestCase(
    GmpGetSystemReportsTestMixin, Gmpv225TestCase
):
    pass
