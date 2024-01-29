# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208.entities.targets import (
    GmpCloneTargetTestMixin,
    GmpDeleteTargetTestMixin,
    GmpGetTargetsTestMixin,
    GmpGetTargetTestMixin,
)
from ...gmpv224.entities.targets import (
    GmpCreateTargetTestMixin,
    GmpModifyTargetTestMixin,
)
from ...gmpv225 import Gmpv225TestCase


class Gmpv225CloneTargetTestCase(GmpCloneTargetTestMixin, Gmpv225TestCase):
    pass


class Gmpv225CreateTargetTestCase(GmpCreateTargetTestMixin, Gmpv225TestCase):
    pass


class Gmpv225DeleteTargetTestCase(GmpDeleteTargetTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetTargetTestCase(GmpGetTargetTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetTargetsTestCase(GmpGetTargetsTestMixin, Gmpv225TestCase):
    pass


class Gmpv225ModifyTargetTestCase(GmpModifyTargetTestMixin, Gmpv225TestCase):
    pass
