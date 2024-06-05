# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224 import Gmpv224TestCase
from .targets import (
    GmpCloneTargetTestMixin,
    GmpCreateTargetTestMixin,
    GmpDeleteTargetTestMixin,
    GmpGetTargetsTestMixin,
    GmpGetTargetTestMixin,
    GmpModifyTargetTestMixin,
)


class Gmpv224CloneTargetTestCase(GmpCloneTargetTestMixin, Gmpv224TestCase):
    pass


class Gmpv224CreateTargetTestCase(GmpCreateTargetTestMixin, Gmpv224TestCase):
    pass


class Gmpv224DeleteTargetTestCase(GmpDeleteTargetTestMixin, Gmpv224TestCase):
    pass


class Gmpv224GetTargetTestCase(GmpGetTargetTestMixin, Gmpv224TestCase):
    pass


class Gmpv224GetTargetsTestCase(GmpGetTargetsTestMixin, Gmpv224TestCase):
    pass


class Gmpv224ModifyTargetTestCase(GmpModifyTargetTestMixin, Gmpv224TestCase):
    pass
