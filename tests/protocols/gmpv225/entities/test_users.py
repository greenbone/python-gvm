# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208.entities.users import (
    GmpCloneUserTestMixin,
    GmpDeleteUserTestMixin,
    GmpGetUsersTestMixin,
    GmpGetUserTestMixin,
)
from ...gmpv224.entities.users import (
    GmpCreateUserTestMixin,
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
