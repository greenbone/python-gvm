# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208 import Gmpv208TestCase
from .users import (
    GmpCloneUserTestMixin,
    GmpCreateUserTestMixin,
    GmpDeleteUserTestMixin,
    GmpGetUsersTestMixin,
    GmpGetUserTestMixin,
    GmpModifyUserTestMixin,
)


class Gmpv208DeleteUserTestCase(GmpDeleteUserTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetUserTestCase(GmpGetUserTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetUsersTestCase(GmpGetUsersTestMixin, Gmpv208TestCase):
    pass


class Gmpv208CloneUserTestCase(GmpCloneUserTestMixin, Gmpv208TestCase):
    pass


class Gmpv208CreateUserTestCase(GmpCreateUserTestMixin, Gmpv208TestCase):
    pass


class Gmpv208ModifyUserTestCase(GmpModifyUserTestMixin, Gmpv208TestCase):
    pass
