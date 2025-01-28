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
from ...gmpv225 import GMPTestCase


class Gmpv225DeleteGroupTestCase(GmpDeleteGroupTestMixin, GMPTestCase):
    pass


class Gmpv225GetGroupTestCase(GmpGetGroupTestMixin, GMPTestCase):
    pass


class Gmpv225GetGroupsTestCase(GmpGetGroupsTestMixin, GMPTestCase):
    pass


class Gmpv225CloneGroupTestCase(GmpCloneGroupTestMixin, GMPTestCase):
    pass


class Gmpv225CreateGroupTestCase(GmpCreateGroupTestMixin, GMPTestCase):
    pass


class Gmpv225ModifyGroupTestCase(GmpModifyGroupTestMixin, GMPTestCase):
    pass
