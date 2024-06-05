# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224 import Gmpv224TestCase
from .groups import (
    GmpCloneGroupTestMixin,
    GmpCreateGroupTestMixin,
    GmpDeleteGroupTestMixin,
    GmpGetGroupsTestMixin,
    GmpGetGroupTestMixin,
    GmpModifyGroupTestMixin,
)


class Gmpv224DeleteGroupTestCase(GmpDeleteGroupTestMixin, Gmpv224TestCase):
    pass


class Gmpv224GetGroupTestCase(GmpGetGroupTestMixin, Gmpv224TestCase):
    pass


class Gmpv224GetGroupsTestCase(GmpGetGroupsTestMixin, Gmpv224TestCase):
    pass


class Gmpv224CloneGroupTestCase(GmpCloneGroupTestMixin, Gmpv224TestCase):
    pass


class Gmpv224CreateGroupTestCase(GmpCreateGroupTestMixin, Gmpv224TestCase):
    pass


class Gmpv224ModifyGroupTestCase(GmpModifyGroupTestMixin, Gmpv224TestCase):
    pass
