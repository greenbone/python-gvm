# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208.entities.targets import (
    GmpCloneTargetTestMixin,
    GmpDeleteTargetTestMixin,
    GmpGetTargetsTestMixin,
    GmpGetTargetTestMixin,
)
from ...gmpv214 import Gmpv214TestCase
from .targets import GmpCreateTargetTestMixin, GmpModifyTargetTestMixin


class Gmpv214CloneTargetTestCase(GmpCloneTargetTestMixin, Gmpv214TestCase):
    pass


class Gmpv214CreateTargetTestCase(GmpCreateTargetTestMixin, Gmpv214TestCase):
    pass


class Gmpv214DeleteTargetTestCase(GmpDeleteTargetTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetTargetTestCase(GmpGetTargetTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetTargetsTestCase(GmpGetTargetsTestMixin, Gmpv214TestCase):
    pass


class Gmpv214ModifyTargetTestCase(GmpModifyTargetTestMixin, Gmpv214TestCase):
    pass
