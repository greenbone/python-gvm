# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208 import Gmpv208TestCase
from .targets import (
    GmpCloneTargetTestMixin,
    GmpCreateTargetTestMixin,
    GmpDeleteTargetTestMixin,
    GmpGetTargetsTestMixin,
    GmpGetTargetTestMixin,
    GmpModifyTargetTestMixin,
)


class Gmpv208CloneTargetTestCase(GmpCloneTargetTestMixin, Gmpv208TestCase):
    pass


class Gmpv208CreateTargetTestCase(GmpCreateTargetTestMixin, Gmpv208TestCase):
    pass


class Gmpv208DeleteTargetTestCase(GmpDeleteTargetTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetTargetTestCase(GmpGetTargetTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetTargetsTestCase(GmpGetTargetsTestMixin, Gmpv208TestCase):
    pass


class Gmpv208ModifyTargetTestCase(GmpModifyTargetTestMixin, Gmpv208TestCase):
    pass
