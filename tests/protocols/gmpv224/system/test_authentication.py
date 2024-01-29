# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208.system.authentication import (
    GmpAuthenticateTestMixin,
    GmpDescribeAuthTestMixin,
    GmpModifyAuthTestMixin,
)
from ...gmpv224 import Gmpv224TestCase


class Gmpv224AuthenticateTestCase(GmpAuthenticateTestMixin, Gmpv224TestCase):
    pass


class Gmpv224ModifyAuthTestCase(GmpModifyAuthTestMixin, Gmpv224TestCase):
    pass


class Gmpv224DescribeAuthCommandTestCase(
    GmpDescribeAuthTestMixin, Gmpv224TestCase
):
    pass
