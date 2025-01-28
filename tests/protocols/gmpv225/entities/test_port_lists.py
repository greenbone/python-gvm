# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
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
from ...gmpv225 import GMPTestCase


class Gmpv225ClonePortListTestCase(GmpClonePortListTestMixin, GMPTestCase):
    pass


class Gmpv225CreatePortListTestCase(GmpCreatePortListTestMixin, GMPTestCase):
    pass


class Gmpv225CreatePortRangeListTestCase(
    GmpCreatePortRangeTestMixin, GMPTestCase
):
    pass


class Gmpv225DeletePortListTestCase(GmpDeletePortListTestMixin, GMPTestCase):
    pass


class Gmpv225DeletePortRangeTestCase(GmpDeletePortRangeTestMixin, GMPTestCase):
    pass


class Gmpv225GetPortListTestCase(GmpGetPortListTestMixin, GMPTestCase):
    pass


class Gmpv225GetPortListsTestCase(GmpGetPortListsTestMixin, GMPTestCase):
    pass


class Gmpv225ModifyPortListTestCase(GmpModifyPortListTestMixin, GMPTestCase):
    pass
