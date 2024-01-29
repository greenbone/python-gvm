# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208 import Gmpv208TestCase
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


class Gmpv208ClonePortListTestCase(GmpClonePortListTestMixin, Gmpv208TestCase):
    pass


class Gmpv208CreatePortListTestCase(
    GmpCreatePortListTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208CreatePortRangeListTestCase(
    GmpCreatePortRangeTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208DeletePortListTestCase(
    GmpDeletePortListTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208DeletePortRangeTestCase(
    GmpDeletePortRangeTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208GetPortListTestCase(GmpGetPortListTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetPortListsTestCase(GmpGetPortListsTestMixin, Gmpv208TestCase):
    pass


class Gmpv208ModifyPortListTestCase(
    GmpModifyPortListTestMixin, Gmpv208TestCase
):
    pass
