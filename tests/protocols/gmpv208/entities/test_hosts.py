# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208 import Gmpv208TestCase
from .hosts import (
    GmpCreateHostTestMixin,
    GmpDeleteHostTestMixin,
    GmpGetHostsTestMixin,
    GmpGetHostTestMixin,
    GmpModifyHostTestMixin,
)


class Gmpv208CreateHostTestCase(GmpCreateHostTestMixin, Gmpv208TestCase):
    pass


class Gmpv208DeleteHostTestCase(GmpDeleteHostTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetHostTestCase(GmpGetHostTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetHostsTestCase(GmpGetHostsTestMixin, Gmpv208TestCase):
    pass


class Gmpv208ModifyHostTestCase(GmpModifyHostTestMixin, Gmpv208TestCase):
    pass
