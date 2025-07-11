# SPDX-FileCopyrightText: 2023-2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224.entities.port_lists import (
    GmpClonePortListTestMixin,
    GmpCreatePortListTestMixin,
    GmpCreatePortRangeTestMixin,
    GmpDeletePortListTestMixin,
    GmpDeletePortRangeTestMixin,
    GmpGetPortListsTestMixin,
    GmpGetPortListTestMixin,
    GmpModifyPortListTestMixin,
)
from ...gmpv227 import GMPTestCase


class GMPClonePortListTestCase(GmpClonePortListTestMixin, GMPTestCase):
    pass


class GMPCreatePortListTestCase(GmpCreatePortListTestMixin, GMPTestCase):
    pass


class GMPCreatePortRangeListTestCase(GmpCreatePortRangeTestMixin, GMPTestCase):
    pass


class GMPDeletePortListTestCase(GmpDeletePortListTestMixin, GMPTestCase):
    pass


class GMPDeletePortRangeTestCase(GmpDeletePortRangeTestMixin, GMPTestCase):
    pass


class GMPGetPortListTestCase(GmpGetPortListTestMixin, GMPTestCase):
    pass


class GMPGetPortListsTestCase(GmpGetPortListsTestMixin, GMPTestCase):
    pass


class GMPModifyPortListTestCase(GmpModifyPortListTestMixin, GMPTestCase):
    pass
