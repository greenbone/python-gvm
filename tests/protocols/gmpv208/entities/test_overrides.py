# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208 import Gmpv208TestCase
from .overrides import (
    GmpCloneOverrideTestMixin,
    GmpCreateOverrideTestMixin,
    GmpDeleteOverrideTestMixin,
    GmpGetOverridesTestMixin,
    GmpGetOverrideTestMixin,
    GmpModifyOverrideTestMixin,
)


class Gmpv208CloneOverrideTestCase(GmpCloneOverrideTestMixin, Gmpv208TestCase):
    pass


class Gmpv208CreateOverrideTestCase(
    GmpCreateOverrideTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208DeleteOverrideTestCase(
    GmpDeleteOverrideTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208GetOverrideTestCase(GmpGetOverrideTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetOverridesTestCase(GmpGetOverridesTestMixin, Gmpv208TestCase):
    pass


class Gmpv208ModifyOverrideTestCase(
    GmpModifyOverrideTestMixin, Gmpv208TestCase
):
    pass
