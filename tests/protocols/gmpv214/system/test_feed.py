# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208.system.feed import GmpGetFeedsTestMixin, GmpGetFeedTestMixin
from ...gmpv214 import Gmpv214TestCase


class Gmpv214GetFeedTestCase(GmpGetFeedTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetFeedsTestCase(GmpGetFeedsTestMixin, Gmpv214TestCase):
    pass
