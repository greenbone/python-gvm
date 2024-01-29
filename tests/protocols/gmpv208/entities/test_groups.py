# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208 import Gmpv208TestCase
from .groups import (
    GmpCloneGroupTestMixin,
    GmpCreateGroupTestMixin,
    GmpDeleteGroupTestMixin,
    GmpGetGroupsTestMixin,
    GmpGetGroupTestMixin,
    GmpModifyGroupTestMixin,
)


class Gmpv208DeleteGroupTestCase(GmpDeleteGroupTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetGroupTestCase(GmpGetGroupTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetGroupsTestCase(GmpGetGroupsTestMixin, Gmpv208TestCase):
    pass


class Gmpv208CloneGroupTestCase(GmpCloneGroupTestMixin, Gmpv208TestCase):
    pass


class Gmpv208CreateGroupTestCase(GmpCreateGroupTestMixin, Gmpv208TestCase):
    pass


class Gmpv208ModifyGroupTestCase(GmpModifyGroupTestMixin, Gmpv208TestCase):
    pass
