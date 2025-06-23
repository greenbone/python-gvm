# SPDX-FileCopyrightText: 2023-2025 Greenbone AG
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
from ...gmpv227 import GMPTestCase


class GMPCreateHostTestCase(GmpCreateHostTestMixin, GMPTestCase):
    pass


class GMPDeleteHostTestCase(GmpDeleteHostTestMixin, GMPTestCase):
    pass


class GMPGetHostTestCase(GmpGetHostTestMixin, GMPTestCase):
    pass


class GMPGetHostsTestCase(GmpGetHostsTestMixin, GMPTestCase):
    pass


class GMPModifyHostTestCase(GmpModifyHostTestMixin, GMPTestCase):
    pass
