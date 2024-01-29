# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208.entities.users import (
    GmpCloneUserTestMixin,
    GmpDeleteUserTestMixin,
    GmpGetUsersTestMixin,
    GmpGetUserTestMixin,
)
from ...gmpv224 import Gmpv224TestCase
from .users import GmpCreateUserTestMixin, GmpModifyUserTestMixin


class Gmpv224CloneUserTestCase(GmpCloneUserTestMixin, Gmpv224TestCase):
    pass


class Gmpv224CreateUserTestCase(GmpCreateUserTestMixin, Gmpv224TestCase):
    pass


class Gmpv224DeleteUserTestCase(GmpDeleteUserTestMixin, Gmpv224TestCase):
    pass


class Gmpv224GetUserTestCase(GmpGetUserTestMixin, Gmpv224TestCase):
    pass


class Gmpv224GetUsersTestCase(GmpGetUsersTestMixin, Gmpv224TestCase):
    pass


class Gmpv224ModifyUserTestCase(GmpModifyUserTestMixin, Gmpv224TestCase):
    pass
