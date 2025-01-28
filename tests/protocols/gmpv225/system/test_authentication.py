# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224.system.authentication import (
    GmpAuthenticateTestMixin,
    GmpDescribeAuthTestMixin,
    GmpModifyAuthTestMixin,
)
from ...gmpv225 import GMPTestCase


class Gmpv225AuthenticateTestCase(GmpAuthenticateTestMixin, GMPTestCase):
    pass


class Gmpv225ModifyAuthTestCase(GmpModifyAuthTestMixin, GMPTestCase):
    pass


class Gmpv225DescribeAuthCommandTestCase(GmpDescribeAuthTestMixin, GMPTestCase):
    pass
