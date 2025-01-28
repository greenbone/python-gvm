# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224.system.feed import GmpGetFeedsTestMixin, GmpGetFeedTestMixin
from ...gmpv225 import GMPTestCase


class Gmpv225GetFeedTestCase(GmpGetFeedTestMixin, GMPTestCase):
    pass


class Gmpv225GetFeedsTestCase(GmpGetFeedsTestMixin, GMPTestCase):
    pass
