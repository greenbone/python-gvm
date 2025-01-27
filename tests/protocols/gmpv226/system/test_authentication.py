# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224.system.authentication import (
    GmpAuthenticateTestMixin,
    GmpDescribeAuthTestMixin,
    GmpModifyAuthTestMixin,
)
from ...gmpv226 import GMPTestCase


class GMPAuthenticateTestCase(GmpAuthenticateTestMixin, GMPTestCase):
    pass


class GMPModifyAuthTestCase(GmpModifyAuthTestMixin, GMPTestCase):
    pass


class GMPDescribeAuthCommandTestCase(GmpDescribeAuthTestMixin, GMPTestCase):
    pass
