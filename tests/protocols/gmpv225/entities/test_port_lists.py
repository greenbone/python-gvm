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
from ...gmpv225 import Gmpv225TestCase


class Gmpv225ClonePortListTestCase(GmpClonePortListTestMixin, Gmpv225TestCase):
    pass


class Gmpv225CreatePortListTestCase(
    GmpCreatePortListTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225CreatePortRangeListTestCase(
    GmpCreatePortRangeTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225DeletePortListTestCase(
    GmpDeletePortListTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225DeletePortRangeTestCase(
    GmpDeletePortRangeTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225GetPortListTestCase(GmpGetPortListTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetPortListsTestCase(GmpGetPortListsTestMixin, Gmpv225TestCase):
    pass


class Gmpv225ModifyPortListTestCase(
    GmpModifyPortListTestMixin, Gmpv225TestCase
):
    pass
