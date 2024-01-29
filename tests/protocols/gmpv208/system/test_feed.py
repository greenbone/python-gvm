# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208 import Gmpv208TestCase
from .feed import GmpGetFeedsTestMixin, GmpGetFeedTestMixin


class Gmpv208GetFeedTestCase(GmpGetFeedTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetFeedsTestCase(GmpGetFeedsTestMixin, Gmpv208TestCase):
    pass
