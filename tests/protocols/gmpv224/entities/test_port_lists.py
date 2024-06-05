# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224 import Gmpv224TestCase
from .port_lists import (
    GmpClonePortListTestMixin,
    GmpCreatePortListTestMixin,
    GmpCreatePortRangeTestMixin,
    GmpDeletePortListTestMixin,
    GmpDeletePortRangeTestMixin,
    GmpGetPortListsTestMixin,
    GmpGetPortListTestMixin,
    GmpModifyPortListTestMixin,
)


class Gmpv224ClonePortListTestCase(GmpClonePortListTestMixin, Gmpv224TestCase):
    pass


class Gmpv224CreatePortListTestCase(
    GmpCreatePortListTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224CreatePortRangeListTestCase(
    GmpCreatePortRangeTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224DeletePortListTestCase(
    GmpDeletePortListTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224DeletePortRangeTestCase(
    GmpDeletePortRangeTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224GetPortListTestCase(GmpGetPortListTestMixin, Gmpv224TestCase):
    pass


class Gmpv224GetPortListsTestCase(GmpGetPortListsTestMixin, Gmpv224TestCase):
    pass


class Gmpv224ModifyPortListTestCase(
    GmpModifyPortListTestMixin, Gmpv224TestCase
):
    pass
