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
from ...gmpv226 import GMPTestCase


class GMPCloneOverrideTestCase(GmpCloneOverrideTestMixin, GMPTestCase):
    pass


class GMPCreateOverrideTestCase(GmpCreateOverrideTestMixin, GMPTestCase):
    pass


class GMPDeleteOverrideTestCase(GmpDeleteOverrideTestMixin, GMPTestCase):
    pass


class GMPGetOverrideTestCase(GmpGetOverrideTestMixin, GMPTestCase):
    pass


class GMPGetOverridesTestCase(GmpGetOverridesTestMixin, GMPTestCase):
    pass


class GMPModifyOverrideTestCase(GmpModifyOverrideTestMixin, GMPTestCase):
    pass
