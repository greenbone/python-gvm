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
from ...gmpv225 import GMPTestCase


class Gmpv225CreateHostTestCase(GmpCreateHostTestMixin, GMPTestCase):
    pass


class Gmpv225DeleteHostTestCase(GmpDeleteHostTestMixin, GMPTestCase):
    pass


class Gmpv225GetHostTestCase(GmpGetHostTestMixin, GMPTestCase):
    pass


class Gmpv225GetHostsTestCase(GmpGetHostsTestMixin, GMPTestCase):
    pass


class Gmpv225ModifyHostTestCase(GmpModifyHostTestMixin, GMPTestCase):
    pass
