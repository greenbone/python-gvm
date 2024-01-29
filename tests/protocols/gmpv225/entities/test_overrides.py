# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208.entities.overrides import (
    GmpCloneOverrideTestMixin,
    GmpDeleteOverrideTestMixin,
    GmpGetOverridesTestMixin,
    GmpGetOverrideTestMixin,
)
from ...gmpv224.entities.overrides import (
    GmpCreateOverrideTestMixin,
    GmpModifyOverrideTestMixin,
)
from ...gmpv225 import Gmpv225TestCase


class Gmpv225CloneOverrideTestCase(GmpCloneOverrideTestMixin, Gmpv225TestCase):
    pass


class Gmpv225CreateOverrideTestCase(
    GmpCreateOverrideTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225DeleteOverrideTestCase(
    GmpDeleteOverrideTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225GetOverrideTestCase(GmpGetOverrideTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetOverridesTestCase(GmpGetOverridesTestMixin, Gmpv225TestCase):
    pass


class Gmpv225ModifyOverrideTestCase(
    GmpModifyOverrideTestMixin, Gmpv225TestCase
):
    pass
