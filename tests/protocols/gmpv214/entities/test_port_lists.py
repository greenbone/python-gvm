# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208.entities.port_lists import (
    GmpClonePortListTestMixin,
    GmpCreatePortListTestMixin,
    GmpCreatePortRangeTestMixin,
    GmpDeletePortListTestMixin,
    GmpDeletePortRangeTestMixin,
    GmpGetPortListsTestMixin,
    GmpGetPortListTestMixin,
    GmpModifyPortListTestMixin,
)
from ...gmpv214 import Gmpv214TestCase


class Gmpv214ClonePortListTestCase(GmpClonePortListTestMixin, Gmpv214TestCase):
    pass


class Gmpv214CreatePortListTestCase(
    GmpCreatePortListTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214CreatePortRangeListTestCase(
    GmpCreatePortRangeTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214DeletePortListTestCase(
    GmpDeletePortListTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214DeletePortRangeTestCase(
    GmpDeletePortRangeTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214GetPortListTestCase(GmpGetPortListTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetPortListsTestCase(GmpGetPortListsTestMixin, Gmpv214TestCase):
    pass


class Gmpv214ModifyPortListTestCase(
    GmpModifyPortListTestMixin, Gmpv214TestCase
):
    pass
