# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208.system.authentication import (
    GmpAuthenticateTestMixin,
    GmpDescribeAuthTestMixin,
    GmpModifyAuthTestMixin,
)
from ...gmpv214 import Gmpv214TestCase


class Gmpv214AuthenticateTestCase(GmpAuthenticateTestMixin, Gmpv214TestCase):
    pass


class Gmpv214ModifyAuthTestCase(GmpModifyAuthTestMixin, Gmpv214TestCase):
    pass


class Gmpv214DescribeAuthCommandTestCase(
    GmpDescribeAuthTestMixin, Gmpv214TestCase
):
    pass
