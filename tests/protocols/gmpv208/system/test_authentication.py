# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208 import Gmpv208TestCase
from .authentication import (
    GmpAuthenticateTestMixin,
    GmpDescribeAuthTestMixin,
    GmpModifyAuthTestMixin,
)


class Gmpv208AuthenticateTestCase(GmpAuthenticateTestMixin, Gmpv208TestCase):
    pass


class Gmpv208ModifyAuthTestCase(GmpModifyAuthTestMixin, Gmpv208TestCase):
    pass


class Gmpv208DescribeAuthCommandTestCase(
    GmpDescribeAuthTestMixin, Gmpv208TestCase
):
    pass
