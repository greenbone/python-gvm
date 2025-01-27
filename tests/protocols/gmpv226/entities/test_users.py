# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224.entities.users import (
    GmpCloneUserTestMixin,
    GmpCreateUserTestMixin,
    GmpDeleteUserTestMixin,
    GmpGetUsersTestMixin,
    GmpGetUserTestMixin,
    GmpModifyUserTestMixin,
)
from ...gmpv226 import GMPTestCase


class GMPCloneUserTestCase(GmpCloneUserTestMixin, GMPTestCase):
    pass


class GMPCreateUserTestCase(GmpCreateUserTestMixin, GMPTestCase):
    pass


class GMPDeleteUserTestCase(GmpDeleteUserTestMixin, GMPTestCase):
    pass


class GMPGetUserTestCase(GmpGetUserTestMixin, GMPTestCase):
    pass


class GMPGetUsersTestCase(GmpGetUsersTestMixin, GMPTestCase):
    pass


class GMPModifyUserTestCase(GmpModifyUserTestMixin, GMPTestCase):
    pass
