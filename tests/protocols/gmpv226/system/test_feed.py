# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224.system.feed import GmpGetFeedsTestMixin, GmpGetFeedTestMixin
from ...gmpv226 import GMPTestCase


class GMPGetFeedTestCase(GmpGetFeedTestMixin, GMPTestCase):
    pass


class GMPGetFeedsTestCase(GmpGetFeedsTestMixin, GMPTestCase):
    pass
