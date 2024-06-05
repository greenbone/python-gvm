# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224.entities.groups import (
    GmpCloneGroupTestMixin,
    GmpCreateGroupTestMixin,
    GmpDeleteGroupTestMixin,
    GmpGetGroupsTestMixin,
    GmpGetGroupTestMixin,
    GmpModifyGroupTestMixin,
)
from ...gmpv225 import Gmpv225TestCase


class Gmpv225DeleteGroupTestCase(GmpDeleteGroupTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetGroupTestCase(GmpGetGroupTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetGroupsTestCase(GmpGetGroupsTestMixin, Gmpv225TestCase):
    pass


class Gmpv225CloneGroupTestCase(GmpCloneGroupTestMixin, Gmpv225TestCase):
    pass


class Gmpv225CreateGroupTestCase(GmpCreateGroupTestMixin, Gmpv225TestCase):
    pass


class Gmpv225ModifyGroupTestCase(GmpModifyGroupTestMixin, Gmpv225TestCase):
    pass
