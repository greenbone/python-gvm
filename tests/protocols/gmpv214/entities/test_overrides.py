# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208.entities.overrides import (
    GmpCloneOverrideTestMixin,
    GmpDeleteOverrideTestMixin,
    GmpGetOverridesTestMixin,
    GmpGetOverrideTestMixin,
)
from ...gmpv214 import Gmpv214TestCase
from .overrides import GmpCreateOverrideTestMixin, GmpModifyOverrideTestMixin


class Gmpv214CloneOverrideTestCase(GmpCloneOverrideTestMixin, Gmpv214TestCase):
    pass


class Gmpv214CreateOverrideTestCase(
    GmpCreateOverrideTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214DeleteOverrideTestCase(
    GmpDeleteOverrideTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214GetOverrideTestCase(GmpGetOverrideTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetOverridesTestCase(GmpGetOverridesTestMixin, Gmpv214TestCase):
    pass


class Gmpv214ModifyOverrideTestCase(
    GmpModifyOverrideTestMixin, Gmpv214TestCase
):
    pass
