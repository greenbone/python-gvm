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
from ...gmpv225 import GMPTestCase


class Gmpv225CloneUserTestCase(GmpCloneUserTestMixin, GMPTestCase):
    pass


class Gmpv225CreateUserTestCase(GmpCreateUserTestMixin, GMPTestCase):
    pass


class Gmpv225DeleteUserTestCase(GmpDeleteUserTestMixin, GMPTestCase):
    pass


class Gmpv225GetUserTestCase(GmpGetUserTestMixin, GMPTestCase):
    pass


class Gmpv225GetUsersTestCase(GmpGetUsersTestMixin, GMPTestCase):
    pass


class Gmpv225ModifyUserTestCase(GmpModifyUserTestMixin, GMPTestCase):
    pass
