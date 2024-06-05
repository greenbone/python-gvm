# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224 import Gmpv224TestCase
from .aggregates import GmpGetAggregatesTestMixin


class Gmpv224GetAggregatesTestCase(GmpGetAggregatesTestMixin, Gmpv224TestCase):
    pass
