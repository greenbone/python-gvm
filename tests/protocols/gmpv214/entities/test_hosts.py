# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208.entities.hosts import (
    GmpCreateHostTestMixin,
    GmpDeleteHostTestMixin,
    GmpGetHostsTestMixin,
    GmpGetHostTestMixin,
    GmpModifyHostTestMixin,
)
from ...gmpv214 import Gmpv214TestCase


class Gmpv214CreateHostTestCase(GmpCreateHostTestMixin, Gmpv214TestCase):
    pass


class Gmpv214DeleteHostTestCase(GmpDeleteHostTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetHostTestCase(GmpGetHostTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetHostsTestCase(GmpGetHostsTestMixin, Gmpv214TestCase):
    pass


class Gmpv214ModifyHostTestCase(GmpModifyHostTestMixin, Gmpv214TestCase):
    pass
