# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224.entities.overrides import (
    GmpCloneOverrideTestMixin,
    GmpCreateOverrideTestMixin,
    GmpDeleteOverrideTestMixin,
    GmpGetOverridesTestMixin,
    GmpGetOverrideTestMixin,
    GmpModifyOverrideTestMixin,
)
from ...gmpv225 import GMPTestCase


class Gmpv225CloneOverrideTestCase(GmpCloneOverrideTestMixin, GMPTestCase):
    pass


class Gmpv225CreateOverrideTestCase(GmpCreateOverrideTestMixin, GMPTestCase):
    pass


class Gmpv225DeleteOverrideTestCase(GmpDeleteOverrideTestMixin, GMPTestCase):
    pass


class Gmpv225GetOverrideTestCase(GmpGetOverrideTestMixin, GMPTestCase):
    pass


class Gmpv225GetOverridesTestCase(GmpGetOverridesTestMixin, GMPTestCase):
    pass


class Gmpv225ModifyOverrideTestCase(GmpModifyOverrideTestMixin, GMPTestCase):
    pass
