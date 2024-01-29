# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208.entities.groups import (
    GmpCloneGroupTestMixin,
    GmpCreateGroupTestMixin,
    GmpDeleteGroupTestMixin,
    GmpGetGroupsTestMixin,
    GmpGetGroupTestMixin,
    GmpModifyGroupTestMixin,
)
from ...gmpv214 import Gmpv214TestCase


class Gmpv214DeleteGroupTestCase(GmpDeleteGroupTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetGroupTestCase(GmpGetGroupTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetGroupsTestCase(GmpGetGroupsTestMixin, Gmpv214TestCase):
    pass


class Gmpv214CloneGroupTestCase(GmpCloneGroupTestMixin, Gmpv214TestCase):
    pass


class Gmpv214CreateGroupTestCase(GmpCreateGroupTestMixin, Gmpv214TestCase):
    pass


class Gmpv214ModifyGroupTestCase(GmpModifyGroupTestMixin, Gmpv214TestCase):
    pass
