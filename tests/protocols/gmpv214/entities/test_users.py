# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208.entities.users import (
    GmpCloneUserTestMixin,
    GmpCreateUserTestMixin,
    GmpDeleteUserTestMixin,
    GmpGetUsersTestMixin,
    GmpGetUserTestMixin,
)
from ...gmpv214 import Gmpv214TestCase
from .users import GmpModifyUserTestMixin


class Gmpv214CloneUserTestCase(GmpCloneUserTestMixin, Gmpv214TestCase):
    pass


class Gmpv214CreateUserTestCase(GmpCreateUserTestMixin, Gmpv214TestCase):
    pass


class Gmpv214DeleteUserTestCase(GmpDeleteUserTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetUserTestCase(GmpGetUserTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetUsersTestCase(GmpGetUsersTestMixin, Gmpv214TestCase):
    pass


class Gmpv214ModifyUserTestCase(GmpModifyUserTestMixin, Gmpv214TestCase):
    pass
