# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224 import Gmpv224TestCase
from .feed import GmpGetFeedsTestMixin, GmpGetFeedTestMixin


class Gmpv224GetFeedTestCase(GmpGetFeedTestMixin, Gmpv224TestCase):
    pass


class Gmpv224GetFeedsTestCase(GmpGetFeedsTestMixin, Gmpv224TestCase):
    pass
