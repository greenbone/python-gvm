# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224.entities.hosts import (
    GmpCreateHostTestMixin,
    GmpDeleteHostTestMixin,
    GmpGetHostsTestMixin,
    GmpGetHostTestMixin,
    GmpModifyHostTestMixin,
)
from ...gmpv225 import Gmpv225TestCase


class Gmpv225CreateHostTestCase(GmpCreateHostTestMixin, Gmpv225TestCase):
    pass


class Gmpv225DeleteHostTestCase(GmpDeleteHostTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetHostTestCase(GmpGetHostTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetHostsTestCase(GmpGetHostsTestMixin, Gmpv225TestCase):
    pass


class Gmpv225ModifyHostTestCase(GmpModifyHostTestMixin, Gmpv225TestCase):
    pass
