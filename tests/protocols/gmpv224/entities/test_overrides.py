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
from ...gmpv224 import Gmpv224TestCase
from .overrides import GmpCreateOverrideTestMixin, GmpModifyOverrideTestMixin


class Gmpv224CloneOverrideTestCase(GmpCloneOverrideTestMixin, Gmpv224TestCase):
    pass


class Gmpv224CreateOverrideTestCase(
    GmpCreateOverrideTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224DeleteOverrideTestCase(
    GmpDeleteOverrideTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224GetOverrideTestCase(GmpGetOverrideTestMixin, Gmpv224TestCase):
    pass


class Gmpv224GetOverridesTestCase(GmpGetOverridesTestMixin, Gmpv224TestCase):
    pass


class Gmpv224ModifyOverrideTestCase(
    GmpModifyOverrideTestMixin, Gmpv224TestCase
):
    pass
