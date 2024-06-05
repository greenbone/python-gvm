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
from ...gmpv225 import Gmpv225TestCase


class Gmpv225CloneUserTestCase(GmpCloneUserTestMixin, Gmpv225TestCase):
    pass


class Gmpv225CreateUserTestCase(GmpCreateUserTestMixin, Gmpv225TestCase):
    pass


class Gmpv225DeleteUserTestCase(GmpDeleteUserTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetUserTestCase(GmpGetUserTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetUsersTestCase(GmpGetUsersTestMixin, Gmpv225TestCase):
    pass


class Gmpv225ModifyUserTestCase(GmpModifyUserTestMixin, Gmpv225TestCase):
    pass
