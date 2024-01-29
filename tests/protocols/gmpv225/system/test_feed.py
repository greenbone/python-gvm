# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208.system.feed import GmpGetFeedsTestMixin, GmpGetFeedTestMixin
from ...gmpv225 import Gmpv225TestCase


class Gmpv225GetFeedTestCase(GmpGetFeedTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetFeedsTestCase(GmpGetFeedsTestMixin, Gmpv225TestCase):
    pass
