# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224.system.authentication import (
    GmpAuthenticateTestMixin,
    GmpDescribeAuthTestMixin,
    GmpModifyAuthTestMixin,
)
from ...gmpv225 import Gmpv225TestCase


class Gmpv225AuthenticateTestCase(GmpAuthenticateTestMixin, Gmpv225TestCase):
    pass


class Gmpv225ModifyAuthTestCase(GmpModifyAuthTestMixin, Gmpv225TestCase):
    pass


class Gmpv225DescribeAuthCommandTestCase(
    GmpDescribeAuthTestMixin, Gmpv225TestCase
):
    pass
