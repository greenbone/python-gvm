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
from ...gmpv226 import GMPTestCase


class GMPDeleteGroupTestCase(GmpDeleteGroupTestMixin, GMPTestCase):
    pass


class GMPGetGroupTestCase(GmpGetGroupTestMixin, GMPTestCase):
    pass


class GMPGetGroupsTestCase(GmpGetGroupsTestMixin, GMPTestCase):
    pass


class GMPCloneGroupTestCase(GmpCloneGroupTestMixin, GMPTestCase):
    pass


class GMPCreateGroupTestCase(GmpCreateGroupTestMixin, GMPTestCase):
    pass


class GMPModifyGroupTestCase(GmpModifyGroupTestMixin, GMPTestCase):
    pass
