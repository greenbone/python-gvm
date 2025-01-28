# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224.entities.targets import (
    GmpCloneTargetTestMixin,
    GmpCreateTargetTestMixin,
    GmpDeleteTargetTestMixin,
    GmpGetTargetsTestMixin,
    GmpGetTargetTestMixin,
    GmpModifyTargetTestMixin,
)
from ...gmpv225 import GMPTestCase


class Gmpv225CloneTargetTestCase(GmpCloneTargetTestMixin, GMPTestCase):
    pass


class Gmpv225CreateTargetTestCase(GmpCreateTargetTestMixin, GMPTestCase):
    pass


class Gmpv225DeleteTargetTestCase(GmpDeleteTargetTestMixin, GMPTestCase):
    pass


class Gmpv225GetTargetTestCase(GmpGetTargetTestMixin, GMPTestCase):
    pass


class Gmpv225GetTargetsTestCase(GmpGetTargetsTestMixin, GMPTestCase):
    pass


class Gmpv225ModifyTargetTestCase(GmpModifyTargetTestMixin, GMPTestCase):
    pass
